import json

import google.generativeai as genai

from config.settings import GEMINI_API_KEY
from prompts.gemini_prompts import RECEIPT_EXTRACTION_PROMPT

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


def extract_receipt_data(sanitized_text: str) -> dict:
    """
    Extract structured receipt information using Gemini.
    """

    default_response = {
        "merchant": "",
        "purchase_date": "",
        "total_amount": 0,
        "category": "",
        "items": [],
    }

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = (
            f"{RECEIPT_EXTRACTION_PROMPT}\n\n"
            f"Receipt Text:\n{sanitized_text}"
        )

        response = model.generate_content(prompt)

        if not response.text:
            return default_response

        response_text = response.text.strip()

        # Remove markdown code fences if present
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        data = json.loads(response_text)

        return {
            "merchant": data.get("merchant", ""),
            "purchase_date": data.get("purchase_date", ""),
            "total_amount": data.get("total_amount", 0),
            "category": data.get("category", ""),
            "items": data.get("items", []),
        }

    except Exception:
        return default_response