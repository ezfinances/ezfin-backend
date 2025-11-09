import pytest
from sqlalchemy.orm import Session
from src.transactions import repository, schema
from src.database import Base, engine

# Fixture para configurar o banco de dados de teste
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_transaction(test_db):
    transaction_data = schema.TransactionCreate(amount=100.0, description="Test Transaction", timestamp="2025-11-07T00:00:00", user_id=1)
    transaction = repository.create_transaction(test_db, transaction_data)
    assert transaction.amount == 100.0
    assert transaction.description == "Test Transaction"

def test_read_transactions(test_db):
    transactions = repository.get_transactions_by_user(test_db, user_id=1)
    assert len(transactions) > 0

def test_update_transaction(test_db):
    transaction = test_db.query(repository.model.Transaction).first()
    transaction.description = "Updated Description"
    test_db.commit()
    updated_transaction = test_db.query(repository.model.Transaction).first()
    assert updated_transaction.description == "Updated Description"

@pytest.mark.parametrize("amount, description, timestamp, user_id", [
    (100.0, "Transaction 1", "2025-11-07T00:00:00", 1),
    (200.0, "Transaction 2", "2025-11-08T00:00:00", 2),
    (300.0, "Transaction 3", "2025-11-09T00:00:00", 3),
])
def test_create_transaction_parametrized(test_db, amount, description, timestamp, user_id):
    transaction_data = schema.TransactionCreate(
        amount=amount, description=description, timestamp=timestamp, user_id=user_id
    )
    transaction = repository.create_transaction(test_db, transaction_data)
    assert transaction.amount == amount
    assert transaction.description == description