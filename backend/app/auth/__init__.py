"""Authentication and authorization module"""

from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
)
from app.auth.password import (
    hash_password,
    verify_password,
)
from app.auth.dependencies import (
    get_current_user,
    get_current_active_user,
    require_role,
)
from app.auth.oauth import (
    get_oauth_provider,
    verify_oauth_token,
)

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "decode_token",
    "hash_password",
    "verify_password",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "get_oauth_provider",
    "verify_oauth_token",
]
