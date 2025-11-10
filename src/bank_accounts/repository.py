"""gerencia as operações das contas bancárias dos usuários"""

from sqlalchemy.orm import Session
from src.bank_accounts import model, schema

def create_bank_account(db: Session, bank_account: schema.BankAccountCreate, user_id: int):
    db_bank_account = model.BankAccount(
        user_id=user_id,
        account_name=bank_account.account_name,
        account_number=bank_account.account_number,
        bank_name=bank_account.bank_name,
    )
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account

def get_bank_accounts_by_user(db: Session, user_id: int):
    return db.query(model.BankAccount).filter(model.BankAccount.user_id == user_id).all()
