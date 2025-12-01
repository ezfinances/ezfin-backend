"""gerencia as operações das contas bancárias dos usuários"""

from sqlalchemy.orm import Session
from src.bank_accounts import model, schema
from fastapi import HTTPException
import uuid

def create_bank_account(db: Session, bank_account: schema.BankAccountCreate, user_id: int):
    # Gera um número de conta único automaticamente
    account_number = str(uuid.uuid4())[:12]
    
    db_bank_account = model.BankAccount(
        user_id=user_id,
        account_name=bank_account.account_name,
        account_number=account_number,
        bank_name=bank_account.bank_name,
        account_type=bank_account.account_type,
        status="active",
        balance=0.0,
    )
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account

def get_bank_accounts_by_user(db: Session, user_id: int):
    return db.query(model.BankAccount).filter(model.BankAccount.user_id == user_id).all()

def delete_bank_account(db: Session, account_id: int, user_id: int):
    # Primeiro tenta encontrar a conta do usuário
    account = db.query(model.BankAccount).filter(
        model.BankAccount.id == account_id,
        model.BankAccount.user_id == user_id
    ).first()
    
    if account:
        db.delete(account)
        db.commit()
        return None
    
    # Se não encontrou, tenta sem user_id (debug)
    account = db.query(model.BankAccount).filter(
        model.BankAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    
    # Retorna erro informando que a conta pertence a outro usuário
    raise HTTPException(
        status_code=403, 
        detail=f"Account belongs to user {account.user_id}, but current user is {user_id}"
    )