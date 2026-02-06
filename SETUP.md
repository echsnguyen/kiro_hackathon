# ECH Scribe - Setup Guide

This guide will help you set up the ECH Scribe development environment.

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Redis 7+** - [Download](https://redis.io/download)
- **Docker & Docker Compose** (optional) - [Download](https://www.docker.com/products/docker-desktop)

## Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd allied-health-assessment-automator

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## Manual Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and configure your settings
# At minimum, set:
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - JWT_SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - ENCRYPTION_KEY (generate with: python -c "import base64; import os; print(base64.b64encode(os.urandom(32)).decode())")
# - DATABASE_URL
# - REDIS_URL

# Create PostgreSQL database
createdb allied_health_db
createdb allied_health_test_db

# Enable pgcrypto extension
psql allied_health_db -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
psql allied_health_test_db -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env and configure your settings

# Start the development server
npm run dev
```

### 3. Start Celery Worker (for async tasks)

In a new terminal:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
celery -A app.celery_app worker --loglevel=info
```

## Database Migrations

### Create a new migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest --cov=app          # With coverage report
pytest -m unit            # Run only unit tests
pytest -m property        # Run only property-based tests
```

### Frontend Tests

```bash
cd frontend
npm test                  # Run all tests
npm run test:watch        # Watch mode
npm run test:coverage     # With coverage report
```

## Environment Variables

### Backend (.env)

Key environment variables to configure:

```bash
# Security (REQUIRED - generate secure random values)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-base64-encoded-encryption-key

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/allied_health_db

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# AWS S3 (if using S3 for storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-bucket-name

# AI Services
GOOGLE_API_KEY=your-google-api-key
PYANNOTE_AUTH_TOKEN=your-huggingface-token
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Generating Secure Keys

```bash
# Generate SECRET_KEY and JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY (base64 encoded)
python -c "import base64; import os; print(base64.b64encode(os.urandom(32)).decode())"
```

## Troubleshooting

### Database Connection Issues

1. Ensure PostgreSQL is running:
   ```bash
   # Check status
   pg_isready
   
   # Start PostgreSQL (macOS with Homebrew)
   brew services start postgresql
   
   # Start PostgreSQL (Linux)
   sudo systemctl start postgresql
   ```

2. Verify database exists:
   ```bash
   psql -l | grep allied_health
   ```

### Redis Connection Issues

1. Ensure Redis is running:
   ```bash
   # Check if Redis is running
   redis-cli ping
   # Should return: PONG
   
   # Start Redis (macOS with Homebrew)
   brew services start redis
   
   # Start Redis (Linux)
   sudo systemctl start redis
   ```

### Port Already in Use

If ports 8000 or 5173 are already in use:

```bash
# Backend - change API_PORT in .env
API_PORT=8001

# Frontend - change port in vite.config.ts or use:
npm run dev -- --port 5174
```

### Python Package Installation Issues

If you encounter issues installing Python packages:

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# On macOS, if you have issues with psycopg2:
brew install postgresql
```

## Development Workflow

1. **Start services**: `docker-compose up -d` (or manually start PostgreSQL, Redis, backend, frontend)
2. **Make changes**: Edit code in `backend/` or `frontend/`
3. **Run tests**: `pytest` (backend) or `npm test` (frontend)
4. **Create migrations**: `alembic revision --autogenerate -m "description"`
5. **Apply migrations**: `alembic upgrade head`
6. **Commit changes**: Follow conventional commits format

## Next Steps

After setup is complete:

1. Review the [Requirements Document](.kiro/specs/allied-health-assessment-automator/requirements.md)
2. Review the [Design Document](.kiro/specs/allied-health-assessment-automator/design.md)
3. Check the [Implementation Tasks](.kiro/specs/allied-health-assessment-automator/tasks.md)
4. Start implementing features according to the task list

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
