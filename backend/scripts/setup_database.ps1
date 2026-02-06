# Database setup script for AI Allied Health Assessment Automator (PowerShell)
# This script sets up the database and runs migrations

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Database Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "❌ Error: .env file not found" -ForegroundColor Red
    Write-Host "Please create a .env file based on .env.example"
    Write-Host ""
    Write-Host "Quick setup:"
    Write-Host "  1. Copy-Item .env.example .env"
    Write-Host "  2. Edit .env and set DATABASE_URL and ENCRYPTION_KEY"
    Write-Host "  3. Generate encryption key: python -c `"import os, base64; print(base64.b64encode(os.urandom(32)).decode())`""
    exit 1
}

Write-Host "✓ Found .env file" -ForegroundColor Green
Write-Host ""

# Check if DATABASE_URL is set
$envContent = Get-Content .env -Raw
if ($envContent -notmatch "^DATABASE_URL=") {
    Write-Host "❌ Error: DATABASE_URL not set in .env" -ForegroundColor Red
    exit 1
}

Write-Host "✓ DATABASE_URL is configured" -ForegroundColor Green
Write-Host ""

# Check if ENCRYPTION_KEY is set
if ($envContent -notmatch "^ENCRYPTION_KEY=") {
    Write-Host "❌ Error: ENCRYPTION_KEY not set in .env" -ForegroundColor Red
    Write-Host "Generate one with: python -c `"import os, base64; print(base64.b64encode(os.urandom(32)).decode())`""
    exit 1
}

Write-Host "✓ ENCRYPTION_KEY is configured" -ForegroundColor Green
Write-Host ""

# Check if PostgreSQL is accessible
Write-Host "Checking PostgreSQL connection..."
$checkResult = python -c @"
import sys
import asyncio
from app.database import engine
from sqlalchemy import text

async def check_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text('SELECT 1'))
        print('✓ PostgreSQL connection successful')
        return True
    except Exception as e:
        print(f'❌ PostgreSQL connection failed: {e}')
        return False
    finally:
        await engine.dispose()

sys.exit(0 if asyncio.run(check_connection()) else 1)
"@

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "  1. PostgreSQL is running"
    Write-Host "  2. Database exists (create with: createdb allied_health_db)"
    Write-Host "  3. DATABASE_URL in .env is correct"
    exit 1
}

Write-Host ""

# Run migrations
Write-Host "Running database migrations..."
alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Migration failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Migrations completed successfully" -ForegroundColor Green
Write-Host ""

# Test encryption
Write-Host "Testing encryption setup..."
python scripts/test_encryption.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Encryption tests failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ Database setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Start the API server: uvicorn app.main:app --reload"
Write-Host "  2. View API docs: http://localhost:8000/docs"
Write-Host ""
