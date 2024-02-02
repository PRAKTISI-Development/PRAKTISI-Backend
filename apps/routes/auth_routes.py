# authroutes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.auth_controller import *

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: dict, db: Session = Depends(get_db)):
    return authenticate_user(form_data["userid"], form_data["password"], db)
