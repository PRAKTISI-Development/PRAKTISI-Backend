from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from functools import lru_cache
from apps.database import get_db
from apps.models.users import User
from apps.schemas.user_schema import UserSchema
from apps.helpers.response import response

def create_user(user_data: UserSchema, db: Session = Depends(get_db)):
    try:
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return response(status_code=201, success=True, msg="User created successfully", data=db_user)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@lru_cache
def get_user(userid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == userid).first()
    if user is None:
        return response(status_code=404, success=False, msg="User not found", data=None)
    return response(status_code=200, success=True, msg="User found", data=user)

@lru_cache
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return response(status_code=200, success=True, msg="Users found", data=users)

async def update_user(user_data: UserSchema, userid: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        return response(status_code=404, success=False, msg="User not found", data=None)

    try:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return response(status_code=200, success=True, msg="User updated successfully", data=db_user)
    except HTTPException as e:
        db.rollback()
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_user(userid: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        return response(status_code=404, success=False, msg="User not found", data=None)

    db.delete(db_user)
    db.commit()
    return response(status_code=200, success=True, msg="User deleted successfully", data=None)
