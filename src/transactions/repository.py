"""gerencia as operações de transações das contas bancárias dos usuários"""

from sqlalchemy.orm import Session
from src.transactions import model, schema

def create_transaction(db: Session, transaction: schema.TransactionCreate):
    db_transaction = model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int):
    return db.query(model.Transaction).filter(model.Transaction.user_id == user_id).all()
