from datetime import datetime, timezone

from models.expense_model import expenses_collection


def add_expense(
    user_id: str,
    merchant: str,
    category: str,
    items: list,
    total_amount: float,
    purchase_date: datetime,
    receipt_image: str,
):
    """
    Add a new expense for a user.
    """

    expense_document = {
        "user_id": user_id,
        "merchant": merchant.strip(),
        "category": category.strip(),
        "items": items,
        "total_amount": total_amount,
        "purchase_date": purchase_date,
        "receipt_image": receipt_image,
        "created_at": datetime.now(timezone.utc),
    }

    result = expenses_collection.insert_one(expense_document)

    return {
        "message": "Expense added successfully",
        "expense_id": str(result.inserted_id),
    }


def get_all_expenses(user_id: str):
    """
    Return all expenses belonging to a user.
    """

    expenses = list(expenses_collection.find({"user_id": user_id}))

    for expense in expenses:
        expense["_id"] = str(expense["_id"])

    return expenses