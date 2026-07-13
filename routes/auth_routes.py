from fastapi import APIRouter

from controllers.auth_controller import login, signup
from models.request_model import SignupRequest, LoginRequest

router = APIRouter()


@router.post("/signup")
def signup_endpoint(request: SignupRequest):
    return signup(
        request.full_name,
        request.email,
        request.password,
    )


@router.post("/login")
def login_endpoint(request: LoginRequest):
    return login(
        request.email,
        request.password,
    )