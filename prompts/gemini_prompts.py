# Prompt template for extracting structured data from sanitized receipt text.

RECEIPT_EXTRACTION_PROMPT = """
You are an intelligent receipt parser.

Read the sanitized receipt text and extract the required information.

Return ONLY a valid JSON object.

Do NOT include markdown.
Do NOT include explanations.
Do NOT include extra text.

Use the following JSON format exactly:

{
    "merchant": "",
    "purchase_date": "",
    "total_amount": 0,
    "category": "",
    "items": [
        {
            "name": "",
            "price": 0
        }
    ]
}

If a value is missing, use:
- "" for text fields
- 0 for numeric fields
- [] for the items list

Return ONLY valid JSON.
"""