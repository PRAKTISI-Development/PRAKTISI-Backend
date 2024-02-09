from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.users_controller import *
from apps.schemas.user_schema import UserSchema

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user_endpoint(user_data: UserSchema, db: Session = Depends(get_db)):
    user = create_user(user_data, db)
    return user

@router.get("/{userid}", response_model=None)
async def read_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = get_user(userid, db)
    return user
    
@router.get("/", response_model=None)
async def read_all_users_endpoint(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.put("/{userid}", response_model=None)
async def update_user_endpoint(userid: str, user_data: UserSchema, db: Session = Depends(get_db)):
    user = update_user(user_data, userid, db)
    return user

@router.delete("/{userid}", response_model=None)
def delete_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = delete_user(userid, db)
    return user

