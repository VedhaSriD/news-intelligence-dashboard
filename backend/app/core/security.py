"""
core/security.py
Clerk JWT verification for protected routes.
Verifies the Authorization: Bearer <token> header against Clerk's JWKS.
"""
import logging
from typing import Optional
import httpx
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger   = logging.getLogger(__name__)
bearer   = HTTPBearer(auto_error=False)

# Clerk JWKS URL — tokens are verified against this
CLERK_JWKS_URL = "https://api.clerk.dev/v1/jwks"


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer),
) -> Optional[str]:
    """
    Returns the Clerk user_id from a valid JWT, or None for unauthenticated requests.
    Raises 401 only when called from a protected route via require_user().
    """
    if not credentials:
        return None
    try:
        from jose import jwt, JWTError
        async with httpx.AsyncClient() as client:
            resp = await client.get(CLERK_JWKS_URL)
            jwks = resp.json()
        payload = jwt.decode(
            credentials.credentials,
            jwks,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload.get("sub")
    except Exception as e:
        logger.warning(f"JWT verification failed: {e}")
        return None


async def require_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer),
) -> str:
    """Use as FastAPI dependency on protected routes."""
    user_id = await get_current_user_id(credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_id