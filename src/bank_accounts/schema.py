"""Descrição curta do que esse módulo faz."""

from pydantic import BaseModel

class BankAccountBase(BaseModel):
    account_name: str
    bank_name: str
    account_type: str

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountOut(BankAccountBase):
    id: int
    status: str
    balance: float

    class Config:
        from_attributes = True
