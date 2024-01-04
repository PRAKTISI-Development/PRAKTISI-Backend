from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.praktikan_service import *
from apps.models import Praktikan 
from apps.services import praktikan_service
from apps.database import get_db
from apps.services import auth_service

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: auth_service.OAuth2PasswordRequestForm = Depends()):
    return praktikan_service.login(form_data)

@router.post("/create", response_model=dict)
def create_praktikan_endpoint(praktikan_data: dict, db: Session = Depends(get_db)):
    return create_praktikan(db, praktikan_data)

@router.get("/{nim}", response_model=dict)
def get_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    return get_praktikan(db, nim)

@router.get("/", response_model=list)
def get_praktikans_endpoint(db: Session = Depends(get_db)):
    return get_praktikans(db)

@router.put("/{nim}", response_model=dict)
def update_praktikan_endpoint(nim: str, praktikan_data: dict, db: Session = Depends(get_db)):
    return update_praktikan(db, nim, praktikan_data)

@router.delete("/{nim}", response_model=dict)
def delete_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    return delete_praktikan(db, nim)
