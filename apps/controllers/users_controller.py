from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.users import User 

def create_user(user_data: User, db: Session = Depends(get_db)):
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(userid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == userid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def update_user(user_data: User, userid: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(userid: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

