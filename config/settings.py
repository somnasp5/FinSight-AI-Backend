# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB settings
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Upload folder for file uploads
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

# Tesseract command path
TESSERACT_CMD = os.getenv("TESSERACT_CMD")