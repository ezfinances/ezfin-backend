"""rotas da API para a gestão de contas bancárias"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.bank_accounts import schema, repository
from src.security import get_current_user

router = APIRouter(prefix="/bank-accounts", tags=["Bank Accounts"])

@router.post("/", response_model=schema.BankAccountOut)
def create_bank_account(
    bank_account: schema.BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.create_bank_account(db, bank_account, current_user["id"])

@router.get("/", response_model=list[schema.BankAccountOut])
def get_bank_accounts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_bank_accounts_by_user(db, current_user["id"])

@router.delete("/{account_id}", status_code=204)
def delete_bank_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.delete_bank_account(db, account_id, current_user["id"])