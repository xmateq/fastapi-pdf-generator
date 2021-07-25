from sqlalchemy.orm import Session

from src.database import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
