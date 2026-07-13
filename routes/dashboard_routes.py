from fastapi import APIRouter, Depends

from controllers.dashboard_controller import get_dashboard_data
from middleware.jwt_auth import get_current_user

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    current_user: dict = Depends(get_current_user),
):
    return get_dashboard_data(
        current_user["user_id"]
    )