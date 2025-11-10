from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: str | None = None
    timestamp: datetime

class TransactionCreate(TransactionBase):
    user_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
