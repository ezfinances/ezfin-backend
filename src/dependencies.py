"""Dependências do projeto, incluindo sessão de banco e utilitários para usuários."""

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.users import model

def get_db():
    """Cria uma sessão de banco de dados e garante que seja fechada após o uso."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_username(db: Session, username: str):
    """Retorna um usuário a partir do nome de usuário fornecido."""
    return db.query(model.User).filter(model.User.username == username).first()
