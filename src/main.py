from typing import List

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from passlib.hash import bcrypt

from src.database import SessionLocal, engine, User, Base
from src.schemas import UserCreateSchema, UserDBSchema
from src.auth import AuthHandler
from src import utils

app = FastAPI()
auth_handler = AuthHandler()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserDBSchema)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = User(username=user.username, hashed_password=bcrypt.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(auth_details: UserCreateSchema, db: Session = Depends(get_db)):
    user = utils.get_user_by_username(db, auth_details.username)
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_handler.encode_token(user.username)
    return {"token": token}

@app.get("/profile")
def get_logged_user(username: str = Depends(auth_handler.auth_wrapper)):
    return {"Logged as": username}

@app.get("/users", response_model=List[UserDBSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
