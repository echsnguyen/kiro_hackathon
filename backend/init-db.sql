-- Initialize PostgreSQL database with pgcrypto extension for encryption

-- Enable pgcrypto extension for encryption functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create test database for testing
CREATE DATABASE allied_health_test_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE allied_health_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE allied_health_test_db TO postgres;

-- Note: Actual table schemas will be created by Alembic migrations
