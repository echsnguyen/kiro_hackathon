#!/bin/bash
# Database setup script for AI Allied Health Assessment Automator
# This script sets up the database and runs migrations

set -e  # Exit on error

echo "=========================================="
echo "Database Setup Script"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file based on .env.example"
    echo ""
    echo "Quick setup:"
    echo "  1. cp .env.example .env"
    echo "  2. Edit .env and set DATABASE_URL and ENCRYPTION_KEY"
    echo "  3. Generate encryption key: python -c \"import os, base64; print(base64.b64encode(os.urandom(32)).decode())\""
    exit 1
fi

echo "✓ Found .env file"
echo ""

# Check if DATABASE_URL is set
if ! grep -q "^DATABASE_URL=" .env; then
    echo "❌ Error: DATABASE_URL not set in .env"
    exit 1
fi

echo "✓ DATABASE_URL is configured"
echo ""

# Check if ENCRYPTION_KEY is set
if ! grep -q "^ENCRYPTION_KEY=" .env; then
    echo "❌ Error: ENCRYPTION_KEY not set in .env"
    echo "Generate one with: python -c \"import os, base64; print(base64.b64encode(os.urandom(32)).decode())\""
    exit 1
fi

echo "✓ ENCRYPTION_KEY is configured"
echo ""

# Check if PostgreSQL is accessible
echo "Checking PostgreSQL connection..."
python -c "
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
"

if [ $? -ne 0 ]; then
    echo ""
    echo "Please ensure:"
    echo "  1. PostgreSQL is running"
    echo "  2. Database exists (create with: createdb allied_health_db)"
    echo "  3. DATABASE_URL in .env is correct"
    exit 1
fi

echo ""

# Run migrations
echo "Running database migrations..."
alembic upgrade head

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Migration failed"
    exit 1
fi

echo ""
echo "✓ Migrations completed successfully"
echo ""

# Test encryption
echo "Testing encryption setup..."
python scripts/test_encryption.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Encryption tests failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Database setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start the API server: uvicorn app.main:app --reload"
echo "  2. View API docs: http://localhost:8000/docs"
echo ""
