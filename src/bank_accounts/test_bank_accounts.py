"""Testes de conta bancaria"""

import pytest
from sqlalchemy.orm import Session
from src.bank_accounts import repository, schema
from src.database import Base, engine
from src.users import repository as user_repository, schema as user_schema

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def setup_users(test_db):
    users = [
        user_schema.UserCreate(username="user1", email="user1@example.com", password="password1"),
        user_schema.UserCreate(username="user2", email="user2@example.com", password="password2"),
        user_schema.UserCreate(username="user3", email="user3@example.com", password="password3"),
    ]
    for user in users:
        user_repository.create_user(test_db, user)

@pytest.mark.usefixtures("setup_users")
def test_create_bank_account(test_db):
    account_data = schema.BankAccountCreate(account_name="Test Account", account_number="123456", bank_name="Test Bank", account_type="Checking")
    account = repository.create_bank_account(test_db, account_data, user_id=1)
    assert account.account_name == "Test Account"
    assert account.bank_name == "Test Bank"

@pytest.mark.usefixtures("setup_users")
def test_read_bank_accounts(test_db):
    accounts = repository.get_bank_accounts_by_user(test_db, user_id=1)
    assert len(accounts) > 0

@pytest.mark.usefixtures("setup_users")
def test_update_bank_account(test_db):
    account_data = schema.BankAccountCreate(account_name="Temp Account", account_number="999999", bank_name="Temp Bank", account_type="Savings")
    account = repository.create_bank_account(test_db, account_data, user_id=1)
    account.account_name = "Updated Account Name"
    test_db.commit()
    updated_account = test_db.query(repository.model.BankAccount).filter_by(id=account.id).first()
    assert updated_account.account_name == "Updated Account Name"

@pytest.mark.parametrize("account_name, account_number, bank_name, account_type, user_id", [
    ("Account 1", "111111", "Bank A", "Checking", 1),
    ("Account 2", "222222", "Bank B", "Savings", 2),
    ("Account 3", "333333", "Bank C", "Investment", 3),
])
def test_create_bank_account_parametrized(test_db, account_name, account_number, bank_name, account_type, user_id):
    account_data = schema.BankAccountCreate(
        account_name=account_name, account_number=account_number, bank_name=bank_name, account_type=account_type
    )
    account = repository.create_bank_account(test_db, account_data, user_id=user_id)
    assert account.account_name == account_name
    assert account.bank_name == bank_name
