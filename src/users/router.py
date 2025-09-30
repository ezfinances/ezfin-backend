from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.database import SessionLocal, engine, Base
from src.users import schema, repository, model
from src.security import create_access_token

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schema.UserOut)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = repository.get_user_by_email(db, user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repository.create_user(db, user)

@router.post("/login", response_model=schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
def change_password(
    username: str = Body(...),
    current_password: str = Body(...),
    new_password: str = Body(...),
    new_password_confirm: str = Body(...),
    db: Session = Depends(get_db)
):
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    user = repository.authenticate_user(db, username, current_password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect current password")
    repository.update_user_password(db, user, new_password)
    return {"msg": "Password updated successfully"}