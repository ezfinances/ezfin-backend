from src.database import SessionLocal
from sqlalchemy.orm import Session
from src.users import model

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_username(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()