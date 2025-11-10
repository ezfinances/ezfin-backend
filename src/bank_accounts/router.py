"""rotas da API para a gestão de contas bancárias"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.bank_accounts import schema, repository
from src.users.repository import get_user_by_username
from src.security import get_current_user

router = APIRouter(prefix="/bank-accounts", tags=["Bank Accounts"])

@router.post("/", response_model=schema.BankAccountOut)
def create_bank_account(
    bank_account: schema.BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user = get_user_by_username(db, current_user["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return repository.create_bank_account(db, bank_account, user.id)

@router.get("/", response_model=list[schema.BankAccountOut])
def get_bank_accounts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user = get_user_by_username(db, current_user["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return repository.get_bank_accounts_by_user(db, user.id)
