# ECH Scribe - Project Structure

This document describes the complete project structure for ECH Scribe.

## Overview

```
ech-scribe/
├── backend/                    # Python FastAPI backend
├── frontend/                   # React TypeScript frontend
├── .kiro/                      # Kiro specifications
├── docker-compose.yml          # Docker orchestration
├── Makefile                    # Development commands
├── README.md                   # Project overview
├── SETUP.md                    # Setup instructions
└── .gitignore                  # Git ignore rules
```

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py            # App package initialization
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Application configuration (Pydantic settings)
│   ├── database.py            # Database configuration and session management
│   ├── celery_app.py          # Celery configuration for async tasks
│   │
│   ├── api/                   # API routes
│   │   └── __init__.py        # API router initialization
│   │
│   ├── models/                # SQLAlchemy ORM models
│   │   └── __init__.py        # Models package
│   │
│   ├── schemas/               # Pydantic schemas for validation
│   │   └── __init__.py        # Schemas package
│   │
│   ├── services/              # Business logic services
│   │   └── __init__.py        # Services package
│   │
│   ├── tasks/                 # Celery tasks
│   │   └── __init__.py        # Tasks package
│   │
│   └── utils/                 # Utility functions
│       └── __init__.py        # Utils package
│
├── alembic/                   # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   └── test_health.py         # Health check tests
│
├── alembic.ini                # Alembic configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── .env.example               # Environment variables template
└── init-db.sql                # Database initialization script
```

## Frontend Structure

```
frontend/
├── src/
│   ├── components/            # React components
│   ├── services/              # API client services
│   ├── hooks/                 # Custom React hooks
│   ├── types/                 # TypeScript type definitions
│   ├── store/                 # Zustand state management
│   ├── App.tsx                # Main App component
│   ├── App.css                # App styles
│   ├── App.test.tsx           # App tests
│   ├── main.tsx               # Application entry point
│   ├── index.css              # Global styles
│   ├── vite-env.d.ts          # Vite environment types
│   └── setupTests.ts          # Test configuration
│
├── index.html                 # HTML template
├── package.json               # Node dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── tsconfig.node.json         # TypeScript config for Node
├── vite.config.ts             # Vite configuration
├── jest.config.js             # Jest configuration
├── Dockerfile                 # Docker image definition
└── .env.example               # Environment variables template
```

## Key Technologies

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 16 with SQLAlchemy 2.0
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic 1.13
- **Task Queue**: Celery 5.3 with Redis
- **Testing**: pytest 7.4, Hypothesis 6.98
- **Security**: python-jose, passlib, cryptography
- **AI/ML**: OpenAI Whisper, Google Gemini, pyannote.audio

### Frontend
- **Framework**: React 18.2 with TypeScript
- **Build Tool**: Vite 5.0
- **State Management**: Zustand 4.5
- **Data Fetching**: TanStack Query 5.17
- **HTTP Client**: Axios 1.6
- **Testing**: Jest 29.7, React Testing Library 14.1
- **Routing**: React Router 6.21

### Infrastructure
- **Database**: PostgreSQL 16 with pgcrypto extension
- **Cache/Queue**: Redis 7
- **Storage**: AWS S3 or Azure Blob Storage
- **Containerization**: Docker & Docker Compose

## Configuration Files

### Backend Configuration
- **`.env`**: Environment variables (secrets, API keys, database URLs)
- **`alembic.ini`**: Database migration configuration
- **`pytest.ini`**: Test configuration and markers

### Frontend Configuration
- **`.env`**: Environment variables (API URLs, feature flags)
- **`tsconfig.json`**: TypeScript compiler options
- **`vite.config.ts`**: Vite build and dev server configuration
- **`jest.config.js`**: Jest test runner configuration

## Development Workflow

### 1. Initial Setup
```bash
make setup    # Copy environment files
make install  # Install dependencies
```

### 2. Start Development
```bash
# Option A: Docker (recommended)
make docker-up

# Option B: Manual
make backend-dev    # Terminal 1
make frontend-dev   # Terminal 2
make celery-dev     # Terminal 3
```

### 3. Database Migrations
```bash
make db-migrate msg="Add user table"  # Create migration
make db-upgrade                        # Apply migration
```

### 4. Testing
```bash
make test           # Run all tests
make backend-test   # Backend only
make frontend-test  # Frontend only
```

## Security Features

### Encryption
- **At Rest**: AES-256 encryption for all sensitive data (audio, transcripts, clinical data)
- **In Transit**: TLS 1.2+ for all API communications
- **Database**: PostgreSQL pgcrypto extension for column-level encryption

### Authentication
- **OAuth 2.0**: JWT tokens with Auth0 or AWS Cognito
- **RBAC**: Role-based access control for clinicians
- **Session Management**: Secure token expiration and refresh

### Compliance
- **Audit Logging**: Comprehensive logging of all system events
- **PII Redaction**: Optional redaction of sensitive information
- **Zero Retention**: Private AI instances with no data retention

## Testing Strategy

### Backend Testing
- **Unit Tests**: pytest with markers (`@pytest.mark.unit`)
- **Property Tests**: Hypothesis for property-based testing (`@pytest.mark.property`)
- **Integration Tests**: Full API endpoint testing (`@pytest.mark.integration`)
- **Coverage**: Minimum 70% code coverage

### Frontend Testing
- **Unit Tests**: Jest with React Testing Library
- **Component Tests**: Testing user interactions
- **Integration Tests**: Testing complete user flows
- **Coverage**: Minimum 70% code coverage

## Next Steps

1. ✅ **Task 1 Complete**: Project setup and core infrastructure
2. **Task 2**: Implement data models and database schema
3. **Task 3**: Implement authentication and authorization
4. **Task 4**: Implement audit logging service
5. Continue with remaining tasks in `.kiro/specs/allied-health-assessment-automator/tasks.md`

## Resources

- [Setup Guide](SETUP.md) - Detailed setup instructions
- [Requirements](.kiro/specs/allied-health-assessment-automator/requirements.md) - System requirements
- [Design](.kiro/specs/allied-health-assessment-automator/design.md) - Architecture and design
- [Tasks](.kiro/specs/allied-health-assessment-automator/tasks.md) - Implementation plan
