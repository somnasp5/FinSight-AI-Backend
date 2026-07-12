# Import the database instance from mongo.py
from database.mongo import database

# Get the expenses collection
expenses_collection = database["expenses"]

# Expected Expense document fields:
# - user_id: str (reference to the user)
# - merchant: str
# - category: str
# - items: list (array of purchased items)
# - total_amount: float
# - purchase_date: datetime
# - receipt_image: str (path or URL to the receipt image)
# - created_at: datetime (automatically set on expense creation)
#
# Note: This module only exposes the collection object.
# No schema enforcement is done here; validation should be handled in the service layer.