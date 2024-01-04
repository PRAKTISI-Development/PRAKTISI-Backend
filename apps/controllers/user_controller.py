from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.user_service import create_user, get_user, get_users, update_user, delete_user
from apps.database import get_db

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_user_endpoint(user_data: dict, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.get("/{nim}", response_model=dict)
async def get_user_endpoint(nim: str, db: Session = Depends(get_db)):
    return get_user(db, nim)

@router.get("/", response_model=list)
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

@router.put("/{nim}", response_model=dict)
async def update_user_endpoint(nim: str, user_data: dict, db: Session = Depends(get_db)):
    return update_user(db, nim, user_data)

@router.delete("/{nim}", response_model=dict)
async def delete_user_endpoint(nim: str, db: Session = Depends(get_db)):
    return delete_user(db, nim)
