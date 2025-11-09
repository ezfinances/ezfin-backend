import pytest
from sqlalchemy.orm import Session
from src.users import repository, schema
from src.database import Base, engine

# Fixture para configurar o banco de dados de teste
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    user_data = schema.UserCreate(username="testuser", email="testuser@example.com", password="password")
    user = repository.create_user(test_db, user_data)
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"

def test_read_user(test_db):
    user = repository.get_user_by_username(test_db, "testuser")
    assert user is not None
    assert user.username == "testuser"

def test_update_user(test_db):
    user = repository.get_user_by_username(test_db, "testuser")
    updated_user = repository.update_user(test_db, user, email="newemail@example.com", name=None, password=None)
    assert updated_user.email == "newemail@example.com"

@pytest.mark.parametrize("username, email, password", [
    ("user1", "user1@example.com", "password1"),
    ("user2", "user2@example.com", "password2"),
    ("user3", "user3@example.com", "password3"),
])
def test_create_user_parametrized(test_db, username, email, password):
    user_data = schema.UserCreate(username=username, email=email, password=password)
    user = repository.create_user(test_db, user_data)
    assert user.username == username
    assert user.email == email