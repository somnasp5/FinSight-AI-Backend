# Import MongoDB configuration
from config.settings import MONGODB_URI, DATABASE_NAME

# Import MongoClient from pymongo
from pymongo import MongoClient

# Create a MongoClient instance
client = MongoClient(MONGODB_URI)

# Connect to the database
database = client[DATABASE_NAME]


