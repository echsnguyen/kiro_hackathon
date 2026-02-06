# Database Encryption Setup

This document describes the encryption implementation for the AI Allied Health Assessment Automator database.

## Requirements

**Requirements 7.1, 7.2, 7.3, 7.6, 14.7**: All sensitive data must be encrypted at rest using AES-256 encryption.

## Encryption Strategy

### 1. PostgreSQL pgcrypto Extension

The database uses PostgreSQL's `pgcrypto` extension for column-level encryption. This extension provides:

- **AES-256-GCM encryption**: Industry-standard encryption algorithm
- **pgp_sym_encrypt/pgp_sym_decrypt**: Functions for symmetric encryption
- **Native database encryption**: Encryption happens at the database layer

### 2. Encrypted Fields

The following fields are encrypted at rest:

#### consent_records
- `signature_data`: Digital signature data (TEXT, encrypted)

#### transcripts
- `raw_text`: Full transcript text (TEXT, encrypted)
- `segments`: Transcript segments with diarization (JSONB, encrypted)
- `speakers`: Identified speakers (JSONB, encrypted)

#### clinical_data_records
- `extracted_data`: Extracted clinical data (JSONB, encrypted)
- `validated_data`: Validated assessment data (JSONB, encrypted)
- `validation_status`: Validation status metadata (JSONB, encrypted)

#### submission_records
- `payload`: JSON payload submitted to portal (TEXT, encrypted)

#### audit_logs
- `details`: Event details (JSONB, encrypted)

### 3. Encryption Key Management

**Environment Variable**: `ENCRYPTION_KEY`
- Must be a base64-encoded 256-bit (32-byte) key
- Should be stored in a secure key management system (AWS KMS, Azure Key Vault)
- Must be rotated periodically according to security policy

**Generating a new encryption key**:
```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

### 4. Application-Level Encryption

The `app/encryption.py` module provides utilities for encrypting/decrypting data:

```python
from app.encryption import encryption_service
from app.database import get_db

async def example():
    async with get_db() as db:
        # Encrypt text
        encrypted = await encryption_service.encrypt_text(db, "sensitive data")
        
        # Decrypt text
        decrypted = await encryption_service.decrypt_text(db, encrypted)
        
        # Encrypt JSON
        encrypted_json = await encryption_service.encrypt_json(db, {"key": "value"})
        
        # Decrypt JSON
        decrypted_json = await encryption_service.decrypt_json(db, encrypted_json)
```

### 5. Database Schema

The initial migration (`001_initial_schema.py`) creates:

1. **pgcrypto extension**: Enables encryption functions
2. **All tables**: With proper column types and constraints
3. **Indexes**: For query performance on non-encrypted fields
4. **Triggers**: For automatic timestamp updates
5. **Foreign keys**: For referential integrity

### 6. Performance Considerations

**Indexes**: 
- Encrypted fields cannot be indexed directly
- Indexes are created on non-encrypted fields (IDs, timestamps, status)
- Composite indexes for common query patterns

**Query Performance**:
- Encryption/decryption happens at the database layer
- Minimal performance impact for small to medium datasets
- For large datasets, consider caching decrypted data in application layer

### 7. Compliance

This encryption implementation satisfies:

- **APP (Australian Privacy Principles)**: Data encryption at rest
- **HIPAA**: PHI/PII encryption requirements
- **Requirement 7.1**: Audio files encrypted (via S3/Azure server-side encryption)
- **Requirement 7.2**: Transcript data encrypted at rest
- **Requirement 7.3**: Clinical data encrypted at rest
- **Requirement 7.6**: Consent records encrypted at rest
- **Requirement 14.7**: Audit logs encrypted at rest

## Running Migrations

### Apply migrations
```bash
cd backend
alembic upgrade head
```

### Create a new migration
```bash
cd backend
alembic revision --autogenerate -m "description"
```

### Rollback migration
```bash
cd backend
alembic downgrade -1
```

### View migration history
```bash
cd backend
alembic history
```

### View current version
```bash
cd backend
alembic current
```

## Testing Encryption

To verify encryption is working:

```python
import asyncio
from app.database import AsyncSessionLocal
from app.encryption import encryption_service

async def test_encryption():
    async with AsyncSessionLocal() as db:
        # Test text encryption
        plaintext = "This is sensitive data"
        encrypted = await encryption_service.encrypt_text(db, plaintext)
        decrypted = await encryption_service.decrypt_text(db, encrypted)
        
        assert plaintext == decrypted
        assert encrypted != plaintext
        print(f"✓ Text encryption working")
        
        # Test JSON encryption
        data = {"name": "John Doe", "age": 65}
        encrypted_json = await encryption_service.encrypt_json(db, data)
        decrypted_json = await encryption_service.decrypt_json(db, encrypted_json)
        
        assert data == decrypted_json
        print(f"✓ JSON encryption working")

if __name__ == "__main__":
    asyncio.run(test_encryption())
```

## Security Best Practices

1. **Never commit encryption keys**: Use environment variables or key management systems
2. **Rotate keys regularly**: Implement key rotation policy (e.g., every 90 days)
3. **Backup encrypted data**: Ensure backups include encryption keys (stored separately)
4. **Access control**: Limit access to encryption keys to authorized personnel only
5. **Audit key access**: Log all access to encryption keys
6. **Use TLS in transit**: All data transmission must use TLS 1.2+ (Requirement 7.4)

## Troubleshooting

### Migration fails with "extension pgcrypto does not exist"
Ensure PostgreSQL has pgcrypto extension available:
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Decryption fails with "wrong key"
Verify the `ENCRYPTION_KEY` environment variable matches the key used for encryption.

### Performance issues with encrypted queries
- Ensure indexes are created on non-encrypted fields
- Consider caching frequently accessed decrypted data
- Use connection pooling (already configured in `database.py`)

## Connection Pooling

Connection pooling is configured in `app/database.py`:

```python
engine = create_async_engine(
    settings.database_url,
    pool_size=20,              # Number of connections to maintain
    max_overflow=10,           # Additional connections when pool is full
    pool_pre_ping=True,        # Verify connections before using
)
```

This configuration:
- Maintains 20 persistent connections
- Allows up to 10 additional connections during peak load
- Verifies connection health before use
- Provides optimal performance for concurrent requests

## References

- [PostgreSQL pgcrypto documentation](https://www.postgresql.org/docs/current/pgcrypto.html)
- [Alembic documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy async documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
