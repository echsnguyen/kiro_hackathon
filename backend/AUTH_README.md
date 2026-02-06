# Authentication and Authorization System

This document describes the authentication and authorization implementation for the AI Allied Health Assessment Automator.

## Overview

The system implements OAuth 2.0 with JWT tokens for authentication and role-based access control (RBAC) for authorization. It supports both traditional email/password authentication and OAuth integration with Auth0 and AWS Cognito.

## Features

- **JWT Token Authentication**: Access tokens (30 min) and refresh tokens (7 days)
- **OAuth 2.0 Integration**: Support for Auth0 and AWS Cognito
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access Control (RBAC)**: Admin, Clinician, Supervisor, Viewer roles
- **Token Refresh**: Automatic token refresh mechanism
- **Token Revocation**: Logout invalidates all user tokens
- **Session Management**: Track last login and token versions

## Architecture

### Components

1. **JWT Module** (`app/auth/jwt.py`)
   - Token creation (access and refresh)
   - Token verification and decoding
   - Expiration handling

2. **Password Module** (`app/auth/password.py`)
   - Password hashing with bcrypt
   - Password verification

3. **OAuth Module** (`app/auth/oauth.py`)
   - Auth0 provider implementation
   - AWS Cognito provider implementation
   - Token verification with JWKS

4. **Dependencies Module** (`app/auth/dependencies.py`)
   - FastAPI dependency injection
   - Current user extraction
   - Role-based access control

5. **Auth Service** (`app/services/auth_service.py`)
   - User management
   - Authentication logic
   - Token generation

6. **Auth Routes** (`app/api/routes/auth.py`)
   - Registration endpoint
   - Login endpoints (email/password and OAuth)
   - Token refresh endpoint
   - Logout endpoint
   - User info endpoint

## User Roles

- **ADMIN**: Full system access, user management
- **CLINICIAN**: Can create and manage assessments
- **SUPERVISOR**: Can view and supervise assessments
- **VIEWER**: Read-only access

## API Endpoints

### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "clinician@example.com",
  "password": "SecurePassword123",
  "full_name": "Dr. Jane Smith",
  "role": "clinician"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "clinician@example.com",
  "full_name": "Dr. Jane Smith",
  "role": "clinician",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T12:00:00Z"
}
```

### POST /api/v1/auth/login
Login with email and password.

**Request Body:**
```json
{
  "email": "clinician@example.com",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "clinician@example.com",
    "full_name": "Dr. Jane Smith",
    "role": "clinician",
    "is_active": true,
    "is_verified": true,
    "last_login": "2024-01-15T12:00:00Z",
    "created_at": "2024-01-15T12:00:00Z"
  },
  "token": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

### POST /api/v1/auth/login/oauth
Login with OAuth provider (Auth0 or AWS Cognito).

**Request Body:**
```json
{
  "provider": "auth0",
  "access_token": "oauth_access_token_from_provider"
}
```

**Response:** Same as /login

### POST /api/v1/auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /api/v1/auth/logout
Logout current user (revokes all tokens).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** 204 No Content

### GET /api/v1/auth/me
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "clinician@example.com",
  "full_name": "Dr. Jane Smith",
  "role": "clinician",
  "is_active": true,
  "is_verified": true,
  "last_login": "2024-01-15T12:00:00Z",
  "created_at": "2024-01-15T12:00:00Z"
}
```

### GET /api/v1/auth/verify-token
Verify if the provided token is valid.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "valid": true,
  "user": { ... }
}
```

## Using Authentication in Endpoints

### Require Authentication

```python
from fastapi import APIRouter, Depends
from app.models.user import User
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    return {"message": f"Hello {current_user.full_name}"}
```

### Require Specific Role

```python
from app.auth.dependencies import require_role
from app.models.user import UserRole

@router.post("/admin-only")
async def admin_endpoint(
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    return {"message": "Admin access granted"}
```

### Optional Authentication

```python
from app.auth.dependencies import get_optional_user

@router.get("/public-or-private")
async def mixed_endpoint(
    current_user: User | None = Depends(get_optional_user)
):
    if current_user:
        return {"message": f"Hello {current_user.full_name}"}
    return {"message": "Hello guest"}
```

## Environment Configuration

Add these variables to your `.env` file:

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth Configuration
OAUTH_PROVIDER=auth0  # or 'cognito'

# Auth0 Configuration
OAUTH_DOMAIN=your-tenant.auth0.com
OAUTH_CLIENT_ID=your-auth0-client-id
OAUTH_CLIENT_SECRET=your-auth0-client-secret
OAUTH_AUDIENCE=your-auth0-api-identifier

# AWS Cognito Configuration (alternative)
# OAUTH_DOMAIN=your-user-pool-id
# OAUTH_CLIENT_ID=your-cognito-client-id
# AWS_REGION=us-east-1
```

## OAuth Provider Setup

### Auth0 Setup

1. Create an Auth0 account and application
2. Configure application settings:
   - Application Type: Single Page Application or Regular Web Application
   - Allowed Callback URLs: Your frontend URLs
   - Allowed Web Origins: Your frontend URLs
3. Create an API in Auth0:
   - Set API Identifier (use as OAUTH_AUDIENCE)
   - Enable RBAC if needed
4. Copy Domain, Client ID, Client Secret, and API Identifier to `.env`

### AWS Cognito Setup

1. Create a Cognito User Pool
2. Create an App Client:
   - Enable username/password authentication
   - Configure OAuth flows
3. Configure App Client Settings:
   - Allowed OAuth Flows: Authorization code grant, Implicit grant
   - Allowed OAuth Scopes: email, openid, profile
4. Copy User Pool ID, App Client ID, and Region to `.env`

## Security Considerations

1. **Token Storage**: Store tokens securely in httpOnly cookies or secure storage
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Expiration**: Access tokens expire in 30 minutes, refresh tokens in 7 days
4. **Token Revocation**: Logout invalidates all tokens by rotating token version
5. **Password Requirements**: Minimum 8 characters (enforce stronger rules in production)
6. **Rate Limiting**: Implement rate limiting on authentication endpoints
7. **CORS**: Configure CORS properly for your frontend domains

## Database Migration

Run the migration to create the users table:

```bash
cd backend
alembic upgrade head
```

## Testing

Test the authentication endpoints:

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "full_name": "Test User",
    "role": "clinician"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Get current user (use access_token from login response)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Troubleshooting

### "Invalid token" errors
- Check token expiration
- Verify JWT_SECRET_KEY matches between token creation and verification
- Ensure token is passed correctly in Authorization header

### OAuth verification fails
- Verify OAuth provider configuration
- Check JWKS URL is accessible
- Ensure token is from the correct provider
- Verify audience and issuer match configuration

### User not found after OAuth login
- Check if user was created successfully
- Verify oauth_subject is being stored correctly
- Check database connection

## Future Enhancements

- [ ] Email verification flow
- [ ] Password reset flow
- [ ] Multi-factor authentication (MFA)
- [ ] Session management UI
- [ ] Audit logging for authentication events
- [ ] Rate limiting per user
- [ ] IP-based access control
