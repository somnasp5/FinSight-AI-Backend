# Import the database instance from mongo.py
from database.mongo import database

# Get the users collection
users_collection = database["users"]

# Expected User document fields:
# - full_name: str
# - email: str (should be unique)
# - password: str (hashed, plain text password should never be stored)
# - created_at: datetime (automatically set on account creation)
#
# Note: This module only exposes the collection object.
# No schema enforcement is done here; validation should be handled in the service layer.