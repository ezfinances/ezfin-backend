"""gerencia as operações de transações das contas bancárias dos usuários"""

from sqlalchemy.orm import Session
from src.transactions import model, schema
from src.bank_accounts import model as bank_accounts_model

def create_transaction(db: Session, transaction: schema.TransactionCreate):
    db_transaction = model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Atualizar saldo da conta bancária
    bank_account = db.query(bank_accounts_model.BankAccount).filter(
        bank_accounts_model.BankAccount.id == db_transaction.bank_account_id
    ).first()
    
    if bank_account:
        if db_transaction.transaction_type == "income":
            bank_account.balance += db_transaction.amount
        elif db_transaction.transaction_type == "expense":
            bank_account.balance -= db_transaction.amount
        db.commit()
    
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int):
    return db.query(model.Transaction).filter(model.Transaction.user_id == user_id).all()
