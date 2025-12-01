"""rotas da API para a gestão das transações"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.transactions import repository, schema
from src.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schema.Transaction)
def create_transaction(
    transaction: schema.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Criar transação com user_id do usuário atual
    transaction_data = transaction.dict()
    transaction_data['user_id'] = current_user["id"]
    transaction_obj = schema.TransactionCreate(**transaction_data)
    return repository.create_transaction(db, transaction_obj)

@router.get("/", response_model=list[schema.Transaction])
def get_user_transactions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return repository.get_transactions_by_user(db, current_user["id"])
