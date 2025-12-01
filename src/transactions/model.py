"""Classe transação"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

class Transaction(Base):
    """Representa uma transação de uma conta bancaria"""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    transaction_type = Column(String, nullable=False, default="income")  # income, expense, transfer
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")
