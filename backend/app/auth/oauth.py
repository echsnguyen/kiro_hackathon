"""OAuth 2.0 integration for Auth0 and AWS Cognito"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import httpx
from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.config import settings


class OAuthProvider(ABC):
    """Abstract base class for OAuth providers"""
    
    @abstractmethod
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify OAuth token and return user info"""
        pass
    
    @abstractmethod
    async def get_user_info(self, token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider"""
        pass


class Auth0Provider(OAuthProvider):
    """Auth0 OAuth provider implementation"""
    
    def __init__(self):
        self.domain = settings.oauth_domain
        self.client_id = settings.oauth_client_id
        self.audience = settings.oauth_audience
        self.issuer = f"https://{self.domain}/"
        self.jwks_url = f"https://{self.domain}/.well-known/jwks.json"
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify Auth0 JWT token.
        
        Args:
            token: Auth0 access token
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            # Get JWKS (JSON Web Key Set) from Auth0
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()
                jwks = response.json()
            
            # Decode token header to get key ID
            unverified_header = jwt.get_unverified_header(token)
            
            # Find the signing key
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break
            
            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find appropriate signing key"
                )
            
            # Verify and decode token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer
            )
            
            return payload
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Auth0 token: {str(e)}"
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to verify token with Auth0: {str(e)}"
            )
    
    async def get_user_info(self, token: str) -> Dict[str, Any]:
        """
        Get user information from Auth0.
        
        Args:
            token: Auth0 access token
            
        Returns:
            User information dictionary
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://{self.domain}/userinfo",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to get user info from Auth0: {str(e)}"
            )


class CognitoProvider(OAuthProvider):
    """AWS Cognito OAuth provider implementation"""
    
    def __init__(self):
        self.region = settings.aws_region
        self.user_pool_id = settings.oauth_domain  # Reuse oauth_domain for user pool ID
        self.client_id = settings.oauth_client_id
        self.issuer = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}"
        self.jwks_url = f"{self.issuer}/.well-known/jwks.json"
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify AWS Cognito JWT token.
        
        Args:
            token: Cognito access token
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            # Get JWKS from Cognito
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()
                jwks = response.json()
            
            # Decode token header to get key ID
            unverified_header = jwt.get_unverified_header(token)
            
            # Find the signing key
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break
            
            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find appropriate signing key"
                )
            
            # Verify and decode token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer
            )
            
            return payload
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Cognito token: {str(e)}"
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to verify token with Cognito: {str(e)}"
            )
    
    async def get_user_info(self, token: str) -> Dict[str, Any]:
        """
        Get user information from Cognito token.
        Cognito includes user info in the token itself.
        
        Args:
            token: Cognito access token
            
        Returns:
            User information dictionary
        """
        payload = await self.verify_token(token)
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "email_verified": payload.get("email_verified"),
            "name": payload.get("name"),
        }


# Provider registry
_providers: Dict[str, OAuthProvider] = {}


def get_oauth_provider(provider_name: Optional[str] = None) -> OAuthProvider:
    """
    Get OAuth provider instance.
    
    Args:
        provider_name: Name of the provider ('auth0' or 'cognito').
                      If None, uses the configured default provider.
    
    Returns:
        OAuthProvider instance
        
    Raises:
        HTTPException: If provider is not supported
    """
    if provider_name is None:
        provider_name = settings.oauth_provider
    
    # Return cached provider if available
    if provider_name in _providers:
        return _providers[provider_name]
    
    # Create new provider instance
    if provider_name == "auth0":
        provider = Auth0Provider()
    elif provider_name == "cognito":
        provider = CognitoProvider()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider_name}"
        )
    
    # Cache and return
    _providers[provider_name] = provider
    return provider


async def verify_oauth_token(token: str, provider_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Verify OAuth token and return payload.
    
    Args:
        token: OAuth access token
        provider_name: Name of the provider (optional)
        
    Returns:
        Decoded token payload
    """
    provider = get_oauth_provider(provider_name)
    return await provider.verify_token(token)
