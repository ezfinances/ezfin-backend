"""rotas da API para a criação do relatório"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.security import get_current_user
from src.reports.service import generate_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=dict)
def get_report(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return generate_report(db, current_user["id"])
