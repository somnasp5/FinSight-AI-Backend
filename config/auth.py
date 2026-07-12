# Import JWT settings
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from datetime import datetime, timedelta


def create_access_token(payload: dict) -> str:
    """
    Create a JWT access token with expiration.

    Args:
        payload: Dictionary containing the data to encode in the token

    Returns:
        Encoded JWT token as string
    """
    # Copy payload to avoid modifying the original
    to_encode = payload.copy()

    # Set expiration time
    expire = datetime.utcnow() + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """
    Verify and decode a JWT access token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded payload as dictionary

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    # Decode the token
    decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return decoded_payload