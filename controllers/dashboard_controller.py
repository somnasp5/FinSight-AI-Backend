from datetime import datetime
from bson import ObjectId

from models.expense_model import expenses_collection
from controllers.analytics_controller import serialize_expense


def get_dashboard_data(user_id: str):
    """
    Return summary data required for the dashboard.
    """

    now = datetime.now()

    expenses = list(
    expenses_collection.find(
        {
            "user_id": user_id
        }
    )
)

    total_expenses = sum(
        expense.get("total_amount", 0)
        for expense in expenses
    )

    monthly_expenses = sum(
        expense.get("total_amount", 0)
        for expense in expenses
        if expense["purchase_date"].year == now.year
        and expense["purchase_date"].month == now.month
    )
    
    

    

    total_receipts = len(expenses)

    total_categories = len(
        set(
            expense.get("category", "")
            for expense in expenses
        )
    )

    recent_expenses = (
    expenses_collection.find(
        {
            "user_id": user_id
        }
    )
    .sort("created_at", -1)
    .limit(5)
)

    recent_expenses = [
        serialize_expense(expense)
        for expense in recent_expenses
    ]

    return {
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        "total_receipts": total_receipts,
        "total_categories": total_categories,
        "recent_expenses": recent_expenses,
    }