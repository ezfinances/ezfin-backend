from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: str | None = None
    timestamp: datetime
    transaction_type: str = "income"  # income, expense, transfer
    bank_account_id: int

class TransactionCreate(TransactionBase):
    user_id: int | None = None

class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
