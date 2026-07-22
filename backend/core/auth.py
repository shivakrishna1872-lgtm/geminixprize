from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Mock authentication middleware.
    In a real app, this would use firebase_admin.auth.verify_id_token()
    For now, we accept any token string.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Placeholder for actual verification
    logger.debug(f"Verified token: {token[:10]}...")
    return {"uid": "mock-user-id", "email": "test@antigravity.io"}
