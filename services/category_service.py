def assign_category(merchant: str, items: list) -> str:
    """
    Assign a category using simple keyword matching.
    """

    merchant = merchant.lower()

    item_text = " ".join(
        item.get("name", "").lower()
        for item in items
        if isinstance(item, dict)
    )

    search_text = f"{merchant} {item_text}"

    category_keywords = {
        "Grocery": [
            "dmart",
            "reliance fresh",
            "big bazaar",
            "spencer",
            "easyday",
        ],
        "Food": [
            "swiggy",
            "zomato",
            "restaurant",
            "cafe",
            "coffee",
            "dominos",
            "pizza",
        ],
        "Shopping": [
            "amazon",
            "flipkart",
            "myntra",
            "ajio",
        ],
        "Travel": [
            "uber",
            "ola",
            "rapido",
            "irctc",
        ],
        "Fuel": [
            "indian oil",
            "hp petrol",
            "shell",
        ],
        "Medical": [
            "apollo",
            "medplus",
            "1mg",
            "pharmacy",
        ],
        "Electronics": [
            "croma",
            "reliance digital",
            "vijay sales",
        ],
        "Utilities": [
            "electricity",
            "water bill",
            "gas bill",
            "internet",
        ],
        "Entertainment": [
            "pvr",
            "inox",
            "netflix",
            "bookmyshow",
        ],
    }

    for category, keywords in category_keywords.items():
        if any(keyword in search_text for keyword in keywords):
            return category

    return "Other"