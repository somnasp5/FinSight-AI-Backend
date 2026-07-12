from models.expense_model import expenses_collection
from datetime import datetime


def serialize_expense(expense: dict):
    """
    Convert MongoDB ObjectId and datetime objects into JSON serializable values.
    """
    expense["_id"] = str(expense["_id"])

    if isinstance(expense.get("purchase_date"), datetime):
        expense["purchase_date"] = expense["purchase_date"].isoformat()

    if isinstance(expense.get("created_at"), datetime):
        expense["created_at"] = expense["created_at"].isoformat()

    return expense


def get_category_expenses(user_id: str, year: int, month: int):
    """
    Get total expenses per category for a specific month.
    """

    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "$expr": {
                    "$and": [
                        {"$eq": [{"$year": "$purchase_date"}, year]},
                        {"$eq": [{"$month": "$purchase_date"}, month]},
                    ]
                },
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$total_amount"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "total": "$total",
            }
        },
        {"$sort": {"total": -1}},
    ]

    return list(expenses_collection.aggregate(pipeline))


def get_top_merchants(user_id: str, limit: int = 5):
    """
    Get merchants with the highest total spending.
    """

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$merchant",
                "total": {"$sum": "$total_amount"},
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "merchant": "$_id",
                "total": "$total",
            }
        },
    ]

    return list(expenses_collection.aggregate(pipeline))


def get_total_year_spending(user_id: str, year: int):
    """
    Get total spending for a specific year.
    """

    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "$expr": {
                    "$eq": [{"$year": "$purchase_date"}, year]
                },
            }
        },
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$total_amount"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": year,
                "total": "$total",
            }
        },
    ]

    result = list(expenses_collection.aggregate(pipeline))

    if result:
        return result[0]

    return {
        "year": year,
        "total": 0,
    }


def get_recent_expenses(user_id: str, limit: int = 10):
    """
    Get the most recent expenses.
    """

    expenses = (
        expenses_collection.find({"user_id": user_id})
        .sort("created_at", -1)
        .limit(limit)
    )

    return [serialize_expense(expense) for expense in expenses]