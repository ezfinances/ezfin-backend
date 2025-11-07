from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_name = Column(String, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    bank_name = Column(String, nullable=False)

    user = relationship("User", back_populates="bank_accounts")