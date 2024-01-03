from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services import aslab_service, auth_service
from app.models.aslab import Aslab
from app.models.user import User
from app.database import SessionLocal

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: auth_service.OAuth2PasswordRequestForm = Depends()):
    return aslab_service.login(form_data)
