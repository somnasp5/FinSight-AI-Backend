# Import necessary modules from FastAPI and JWT handling
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.auth import verify_access_token

# Security scheme for extracting the Bearer token from the Authorization header
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to extract and verify the JWT token from the Authorization header.

    Returns the decoded token payload if valid.
    Raises HTTPException 401 if the token is missing, invalid, or expired.
    """
    token = credentials.credentials
    try:
        # Verify and decode the token using the verify_access_token function
        payload = verify_access_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )