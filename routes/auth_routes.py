from fastapi import APIRouter

from controllers.auth_controller import login, signup

router = APIRouter()


@router.post("/signup")
def signup_endpoint(
    full_name: str,
    email: str,
    password: str,
):
    return signup(full_name, email, password)


@router.post("/login")
def login_endpoint(
    email: str,
    password: str,
):
    return login(email, password)