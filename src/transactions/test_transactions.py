"""Testes das transações"""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from src.transactions import repository, schema
from src.bank_accounts import repository as bank_repository, schema as bank_schema
from src.users import repository as user_repository, schema as user_schema
from src.database import Base, engine

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def setup_users_and_accounts(test_db):
    users = [
        user_schema.UserCreate(username="user1", email="user1@example.com", password="password1"),
        user_schema.UserCreate(username="user2", email="user2@example.com", password="password2"),
        user_schema.UserCreate(username="user3", email="user3@example.com", password="password3"),
    ]
    for user in users:
        user_repository.create_user(test_db, user)
    
    #cria contas banncarias pra cada usuario
    for user_id in range(1, 4):
        account_data = bank_schema.BankAccountCreate(
            account_name=f"Account {user_id}",
            account_number=f"12345{user_id}",
            bank_name=f"Bank {user_id}",
            account_type="Checking"
        )
        bank_repository.create_bank_account(test_db, account_data, user_id=user_id)

@pytest.mark.usefixtures("setup_users_and_accounts")
def test_create_transaction(test_db):
    transaction_data = schema.TransactionCreate(
        amount=100.0,
        description="Test Transaction",
        timestamp=datetime(2025, 11, 7),
        bank_account_id=1,
        user_id=1
    )
    transaction = repository.create_transaction(test_db, transaction_data)
    assert transaction.amount == 100.0
    assert transaction.description == "Test Transaction"

@pytest.mark.usefixtures("setup_users_and_accounts")
def test_read_transactions(test_db):
    transactions = repository.get_transactions_by_user(test_db, user_id=1)
    
    assert isinstance(transactions, list)

@pytest.mark.usefixtures("setup_users_and_accounts")
def test_update_transaction(test_db):
    transaction_data = schema.TransactionCreate(
        amount=50.0,
        description="Original Description",
        timestamp=datetime(2025, 11, 7),
        bank_account_id=1,
        user_id=1
    )
    transaction = repository.create_transaction(test_db, transaction_data)
    transaction.description = "Updated Description"
    test_db.commit()
    updated_transaction = test_db.query(repository.model.Transaction).filter_by(id=transaction.id).first()
    assert updated_transaction.description == "Updated Description"

@pytest.mark.usefixtures("setup_users_and_accounts")
@pytest.mark.parametrize("amount, description, bank_account_id, user_id", [
    (100.0, "Transaction 1", 1, 1),
    (200.0, "Transaction 2", 2, 2),
    (300.0, "Transaction 3", 3, 3),
])
def test_create_transaction_parametrized(test_db, amount, description, bank_account_id, user_id):
    transaction_data = schema.TransactionCreate(
        amount=amount,
        description=description,
        timestamp=datetime(2025, 11, 7),
        bank_account_id=bank_account_id,
        user_id=user_id
    )
    transaction = repository.create_transaction(test_db, transaction_data)
    assert transaction.amount == amount
    assert transaction.description == description
