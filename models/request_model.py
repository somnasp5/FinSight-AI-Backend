from datetime import datetime
from typing import List

from pydantic import BaseModel


class ExpenseItem(BaseModel):
    name: str
    price: float


class ExpenseCreateRequest(BaseModel):
    merchant: str
    category: str
    items: List[ExpenseItem]
    total_amount: float
    purchase_date: datetime
    receipt_image: str