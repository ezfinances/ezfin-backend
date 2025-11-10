"""Descrição curta do que esse módulo faz."""

from pydantic import BaseModel

class BankAccountBase(BaseModel):
    account_name: str
    account_number: str
    bank_name: str

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountOut(BankAccountBase):
    id: int

    class Config:
        from_attributes = True
