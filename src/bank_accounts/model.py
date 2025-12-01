"""Classe conta bancaria"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database import Base

class BankAccount(Base):
    """Representa uma conta bancária vinculada a um usuário."""
 
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_name = Column(String, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    bank_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
