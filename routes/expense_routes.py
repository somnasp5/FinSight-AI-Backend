from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from controllers.expense_controller import add_expense, get_all_expenses
from middleware.jwt_auth import get_current_user

router = APIRouter()


class ExpenseItem(BaseModel):
    name: str
    price: float


class ExpenseCreateRequest(BaseModel):
    merchant: str
    category: str
    items: List[ExpenseItem]
    total_amount: float
    purchase_date: datetime
    receipt_image: str


@router.post("/expenses")
def create_expense(
    expense: ExpenseCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Add a new expense for the logged-in user.
    """

    user_id = current_user["user_id"]

    return add_expense(
        user_id=user_id,
        merchant=expense.merchant,
        category=expense.category,
        items=[item.model_dump() for item in expense.items],
        total_amount=expense.total_amount,
        purchase_date=expense.purchase_date,
        receipt_image=expense.receipt_image,
    )


@router.get("/expenses")
def get_expenses(
    current_user: dict = Depends(get_current_user),
):
    """
    Return all expenses for the logged-in user.
    """

    user_id = current_user["user_id"]

    return get_all_expenses(user_id)