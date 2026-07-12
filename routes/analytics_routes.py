from fastapi import APIRouter, Depends

from controllers.analytics_controller import (
    get_category_expenses,
    get_recent_expenses,
    get_top_merchants,
    get_total_year_spending,
)
from middleware.jwt_auth import get_current_user

router = APIRouter()


@router.get("/analytics/category")
def category_expenses(
    year: int,
    month: int,
    current_user: dict = Depends(get_current_user),
):
    return get_category_expenses(
        current_user["user_id"],
        year,
        month,
    )


@router.get("/analytics/merchants")
def top_merchants(
    limit: int = 5,
    current_user: dict = Depends(get_current_user),
):
    return get_top_merchants(
        current_user["user_id"],
        limit,
    )


@router.get("/analytics/year")
def year_spending(
    year: int,
    current_user: dict = Depends(get_current_user),
):
    return get_total_year_spending(
        current_user["user_id"],
        year,
    )


@router.get("/analytics/recent")
def recent_expenses(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
):
    return get_recent_expenses(
        current_user["user_id"],
        limit,
    )