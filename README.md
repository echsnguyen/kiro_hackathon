# ECH Scribe

An integrated clinical documentation tool that transforms audio recordings of client consultations into structured, validated assessment data.

## Technology Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React with TypeScript (Vite)
- **Database**: PostgreSQL with encryption at rest
- **Storage**: AWS S3 / Azure Blob Storage for encrypted audio files
- **Message Queue**: Redis for async processing (Celery)
- **Testing**: pytest, Hypothesis (Python), Jest, React Testing Library (Frontend)

## Project Structure

```
.
├── backend/              # Python FastAPI backend
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   └── requirements.txt # Python dependencies
├── frontend/            # React TypeScript frontend
│   ├── src/            # Frontend source code
│   └── package.json    # Node dependencies
└── docker-compose.yml  # Local development environment
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker (optional, for local development)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Configuration

Copy `.env.example` to `.env` and configure your environment variables.

### Running the Application

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Security

- All PHI/PII encrypted at rest (AES-256) and in transit (TLS 1.2+)
- Human-in-the-loop validation required before portal submission
- Zero data retention with external AI services
- Comprehensive audit logging for compliance

## License

Proprietary - All rights reserved
