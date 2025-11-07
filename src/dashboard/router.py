from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.security import get_current_user
from src.dashboard.service import get_dashboard_data

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=dict)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return get_dashboard_data(db, current_user["id"])