# Import required modules
from datetime import datetime, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext

from config.auth import create_access_token
from models.user_model import users_collection

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(full_name: str, email: str, password: str):
    """
    Register a new user.
    """

    # Normalize email
    email = email.strip().lower()

    # Check if email already exists
    existing_user = users_collection.find_one({"email": email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create user document
    user_document = {
        "full_name": full_name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc),
    }

    # Save user
    result = users_collection.insert_one(user_document)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
    }


def login(email: str, password: str):
    """
    Authenticate a user and generate a JWT token.
    """

    # Normalize email
    email = email.strip().lower()

    # Find user
    user = users_collection.find_one({"email": email})

    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None:
        raise invalid_credentials

    # Verify password
    if not pwd_context.verify(password, user["password"]):
        raise invalid_credentials

    # Create JWT payload
    payload = {
        "user_id": str(user["_id"]),
        "email": user["email"],
    }

    # Generate token
    access_token = create_access_token(payload)

    return {
    "token": access_token,
    "user": {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
    },
}