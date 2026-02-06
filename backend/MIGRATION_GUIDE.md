# Database Migration Guide

This guide explains how to set up and run database migrations for the AI Allied Health Assessment Automator.

## Prerequisites

1. **PostgreSQL 12+** installed and running
2. **Python 3.11+** with virtual environment activated
3. **Environment variables** configured (see `.env.example`)

## Initial Setup

### 1. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/allied_health_db

# Encryption Key (generate with: python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())")
ENCRYPTION_KEY=your_base64_encoded_32_byte_key_here

# Other required variables
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE allied_health_db;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE allied_health_db TO your_username;

# Exit psql
\q
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Running Migrations

### Apply All Migrations

```bash
cd backend
alembic upgrade head
```

This will:
1. Enable the `pgcrypto` extension
2. Create all enum types
3. Create all tables with proper schema
4. Create indexes for query performance
5. Create triggers for automatic timestamp updates

### Check Current Migration Version

```bash
cd backend
alembic current
```

### View Migration History

```bash
cd backend
alembic history --verbose
```

## Testing the Migration

After running migrations, test that everything is set up correctly:

```bash
cd backend
python scripts/test_encryption.py
```

This script will verify:
- ✓ pgcrypto extension is installed
- ✓ Text encryption/decryption works
- ✓ JSON encryption/decryption works
- ✓ All tables are created
- ✓ All indexes are created
- ✓ All enum types are created

Expected output:
```
============================================================
Database Encryption and Schema Tests
============================================================

=== Testing pgcrypto Extension ===
✓ pgcrypto extension is installed

=== Testing Text Encryption ===
Original:  This is sensitive patient data that must be encrypted
Encrypted: c30d04070302...
Decrypted: This is sensitive patient data that must be encrypted
✓ Text is encrypted (differs from plaintext)
✓ Text decryption successful (matches original)

=== Testing JSON Encryption ===
Original:  {'patient_name': 'John Doe', 'age': 65, ...}
Encrypted: c30d04070302...
Decrypted: {'patient_name': 'John Doe', 'age': 65, ...}
✓ JSON encryption/decryption successful

=== Testing Table Creation ===
Found tables: ['audio_recordings', 'audit_logs', 'clinical_data_records', ...]
✓ Table 'consent_records' exists
✓ Table 'audio_recordings' exists
✓ Table 'transcripts' exists
✓ Table 'clinical_data_records' exists
✓ Table 'submission_records' exists
✓ Table 'audit_logs' exists

=== Testing Index Creation ===
Found 25 indexes:
  - consent_records.ix_consent_records_session_id
  - audio_recordings.ix_audio_recordings_session_id
  ...
✓ Critical index 'ix_consent_records_session_id' exists
✓ Critical index 'ix_audio_recordings_session_id' exists
...

=== Testing Enum Types ===
Found enum types: ['consent_method_enum', 'recording_status_enum', ...]
✓ Enum type 'consent_method_enum' exists
✓ Enum type 'recording_status_enum' exists
...

============================================================
Test Summary
============================================================
✓ PASS: pgcrypto Extension
✓ PASS: Text Encryption
✓ PASS: JSON Encryption
✓ PASS: Table Creation
✓ PASS: Index Creation
✓ PASS: Enum Types

Total: 6/6 tests passed

✓ All tests passed! Database encryption is working correctly.
```

## Creating New Migrations

### Auto-generate Migration from Model Changes

```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

This will:
1. Compare current database schema with SQLAlchemy models
2. Generate a migration script with detected changes
3. Save the script in `alembic/versions/`

**Important**: Always review auto-generated migrations before applying them!

### Create Empty Migration

```bash
cd backend
alembic revision -m "description of changes"
```

This creates an empty migration template that you can fill in manually.

## Rolling Back Migrations

### Rollback One Migration

```bash
cd backend
alembic downgrade -1
```

### Rollback to Specific Version

```bash
cd backend
alembic downgrade <revision_id>
```

### Rollback All Migrations

```bash
cd backend
alembic downgrade base
```

## Database Schema Overview

### Tables

1. **consent_records**: Stores consent information
   - Primary key: `consent_id` (UUID)
   - Encrypted fields: `signature_data`
   - Indexes: session_id, clinician_id, client_id

2. **audio_recordings**: Stores audio recording metadata
   - Primary key: `recording_id` (UUID)
   - Foreign key: `consent_record_id` → consent_records
   - Encrypted fields: File stored in S3/Azure with server-side encryption
   - Indexes: session_id, clinician_id, client_id, consent_record_id

3. **transcripts**: Stores transcription results
   - Primary key: `transcript_id` (UUID)
   - Foreign key: `recording_id` → audio_recordings
   - Encrypted fields: `raw_text`, `segments`, `speakers`
   - Indexes: recording_id, session_id

4. **clinical_data_records**: Stores extracted clinical data
   - Primary key: `clinical_data_id` (UUID)
   - Foreign key: `transcript_id` → transcripts
   - Encrypted fields: `extracted_data`, `validated_data`, `validation_status`
   - Indexes: transcript_id, session_id, validated_by, submission_id

5. **submission_records**: Stores portal submission records
   - Primary key: `submission_id` (UUID)
   - Foreign key: `clinical_data_id` → clinical_data_records
   - Encrypted fields: `payload`
   - Indexes: clinical_data_id, session_id, clinician_id, portal_record_id

6. **audit_logs**: Stores audit trail
   - Primary key: `log_id` (UUID)
   - Encrypted fields: `details`
   - Indexes: timestamp, event_type, session_id, clinician_id

### Indexes

The schema includes indexes for:
- All primary keys (UUID)
- All foreign keys
- Frequently queried fields (session_id, clinician_id, timestamps)
- Composite indexes for common query patterns

### Encryption

All sensitive fields are marked for encryption in the schema comments. The application layer handles encryption/decryption using the `app/encryption.py` module.

## Troubleshooting

### Error: "relation already exists"

The table already exists. Either:
1. Drop the database and recreate it
2. Use `alembic downgrade base` to remove all tables
3. Manually drop the conflicting table

### Error: "extension pgcrypto does not exist"

PostgreSQL doesn't have pgcrypto extension. Install it:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-contrib

# macOS (Homebrew)
brew install postgresql
```

Then connect to your database and enable it:
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Error: "asyncpg.exceptions.InvalidPasswordError"

Check your `DATABASE_URL` in `.env`:
- Ensure username and password are correct
- Ensure database exists
- Ensure PostgreSQL is running

### Error: "No module named 'app'"

Ensure you're running commands from the `backend/` directory and the virtual environment is activated.

### Migration Conflicts

If you have migration conflicts:

```bash
# View current state
alembic current

# View history
alembic history

# Stamp database to specific version (use with caution!)
alembic stamp <revision_id>
```

## Best Practices

1. **Always backup** before running migrations in production
2. **Test migrations** in development/staging first
3. **Review auto-generated migrations** before applying
4. **Use transactions** - Alembic wraps migrations in transactions by default
5. **Version control** - Commit migration files to git
6. **Document changes** - Add clear descriptions to migration messages
7. **Test rollbacks** - Ensure downgrade() works correctly

## Production Deployment

### Pre-deployment Checklist

- [ ] Backup production database
- [ ] Test migration in staging environment
- [ ] Review migration SQL (use `alembic upgrade --sql`)
- [ ] Schedule maintenance window if needed
- [ ] Prepare rollback plan

### Deployment Steps

```bash
# 1. Backup database
pg_dump -U username -d allied_health_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Apply migrations
cd backend
alembic upgrade head

# 3. Verify migration
alembic current
python scripts/test_encryption.py

# 4. If issues occur, rollback
alembic downgrade -1
```

### Post-deployment

- [ ] Verify application functionality
- [ ] Check logs for errors
- [ ] Monitor database performance
- [ ] Update documentation

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL pgcrypto](https://www.postgresql.org/docs/current/pgcrypto.html)
- [Encryption README](alembic/README_ENCRYPTION.md)
