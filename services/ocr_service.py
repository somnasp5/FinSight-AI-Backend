from PIL import Image
import pytesseract

from config.settings import TESSERACT_CMD

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_text(image_path: str) -> str:
    """
    Extract text from a receipt image using Tesseract OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text