import re


def sanitize_text(raw_text: str) -> str:
    """
    Clean OCR text and mask sensitive information before sending it to Gemini.
    """

    if not raw_text:
        return raw_text

    # Replace tabs with spaces
    text = raw_text.replace("\t", " ")

    # Replace multiple spaces with a single space
    text = re.sub(r" +", " ", text)

    # Remove extra blank lines
    text = re.sub(r"\n+", "\n", text)

    # Remove leading and trailing whitespace
    text = text.strip()

    # Mask credit/debit card numbers (keep last 4 digits)
    def mask_card(match):
        digits = re.sub(r"\D", "", match.group())

        return "**** **** **** " + digits[-4:]

    text = re.sub(
        r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
        mask_card,
        text,
    )

    # Mask UPI IDs
    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\b",
        "[UPI_ID]",
        text,
    )

    # Mask phone numbers
    text = re.sub(
        r"\b\d{10}\b",
        "[PHONE_NUMBER]",
        text,
    )

    # Mask bank account numbers
    text = re.sub(
        r"\b\d{8,9}\b|\b\d{11,12}\b",
        "[ACCOUNT_NUMBER]",
        text,
    )

    return text