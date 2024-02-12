from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.auth_controller import authenticate_user

router = APIRouter()

@router.post("/login")
async def login_for_access_token(request: Request, form_data: dict, db: Session = Depends(get_db)):
    auth = authenticate_user(request, form_data["userid"], form_data["password"], db)
    try:
        return auth
    except HTTPException as e:
        return { "detail": e.detail }
