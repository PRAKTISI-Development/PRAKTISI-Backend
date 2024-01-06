from sqlalchemy.orm import Session
from apps.models.user import User

def create_user(db: Session, user_data: User):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, nim: str):
    return db.query(User).filter(User.nim == nim).first()

def get_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, nim: str, user_data: User):
    db_user = db.query(User).filter(User.nim == nim).first()
    for key, value in user_data.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, nim: str):
    db_user = db.query(User).filter(User.nim == nim).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
