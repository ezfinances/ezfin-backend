import pytest
from sqlalchemy.orm import Session
from src.reports.service import generate_report
from src.database import Base, engine

# Fixture para configurar o banco de dados de teste
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_generate_report(test_db):
    user_id = 1
    report = generate_report(test_db, user_id)
    assert "total_transactions" in report
    assert "total_spent" in report
    assert "total_received" in report

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_generate_report_parametrized(test_db, user_id):
    report = generate_report(test_db, user_id)
    assert "total_transactions" in report
    assert "total_spent" in report
    assert "total_received" in report