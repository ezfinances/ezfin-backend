from sqlalchemy.orm import Session
from src.users import model, schema
from src.security import get_password_hash, verify_password
from src.dependencies import get_user_by_username

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_password(db: Session, user, new_password: str):
    from src.security import get_password_hash
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user, email: str | None, name: str | None, password: str | None):
    if email:
        user.email = email
    if name:
        user.name = name
    if password:
        from src.security import get_password_hash
        user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user