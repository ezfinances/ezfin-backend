"""Testes do dashboard"""

import pytest
from sqlalchemy.orm import Session
from src.dashboard.service import get_dashboard_data
from src.database import Base, engine

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_dashboard_data(test_db):
    user_id = 1
    dashboard_data = get_dashboard_data(test_db, user_id)
    assert "total_balance" in dashboard_data
    assert "total_spent" in dashboard_data
    assert "total_received" in dashboard_data

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_dashboard_data_parametrized(test_db, user_id):
    dashboard_data = get_dashboard_data(test_db, user_id)
    assert "total_balance" in dashboard_data
    assert "total_spent" in dashboard_data
    assert "total_received" in dashboard_data
