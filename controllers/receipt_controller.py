from datetime import datetime, timezone

from models.expense_model import expenses_collection
from services.category_service import assign_category
from services.gemini_service import extract_receipt_data
from services.ocr_service import extract_text
from services.sanitizer_service import sanitize_text


def process_receipt(user_id: str, image_path: str):
    """
    Process a receipt using the complete pipeline:
    OCR → Sanitizer → Gemini → Category → MongoDB
    """

    # Step 1: OCR
    raw_text = extract_text(image_path)

    # Step 2: Sanitize OCR text
    sanitized_text = sanitize_text(raw_text)

    # Step 3: Gemini extraction
    receipt = extract_receipt_data(sanitized_text)

    merchant = receipt.get("merchant", "")
    purchase_date = receipt.get("purchase_date", "")
    total_amount = receipt.get("total_amount", 0)
    category = receipt.get("category", "")
    items = receipt.get("items", [])

    # Step 4: Fallback category
    if not category:
        category = assign_category(merchant, items)

    # Convert purchase date
    try:
        if purchase_date:
            purchase_date = datetime.fromisoformat(
                purchase_date.replace("Z", "+00:00")
            )
        else:
            purchase_date = datetime.now(timezone.utc)
    except Exception:
        purchase_date = datetime.now(timezone.utc)

    # Step 5: Create expense document
    expense = {
        "user_id": user_id,
        "merchant": merchant,
        "purchase_date": purchase_date,
        "total_amount": total_amount,
        "category": category,
        "items": items,
        "receipt_image": image_path,
        "created_at": datetime.now(timezone.utc),
    }

    result = expenses_collection.insert_one(expense)

    expense["_id"] = str(result.inserted_id)

    return {
        "message": "Receipt processed successfully",
        "expense_id": str(result.inserted_id),
        "expense": expense,
    }