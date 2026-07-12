import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from config.settings import UPLOAD_FOLDER
from controllers.receipt_controller import process_receipt
from middleware.jwt_auth import get_current_user

router = APIRouter()

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/receipt/upload")
def upload_receipt(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a receipt image and process it.
    """

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed",
        )

    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_receipt(
            current_user["user_id"],
            file_path,
        )

        return result

    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise

    finally:
        file.file.close()