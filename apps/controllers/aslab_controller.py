from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.services import aslab_service, auth_service
from apps.models.aslab import Aslab
from apps.models.user import User
from apps.database import SessionLocal
from apps.services.aslab_service import create_aslab, get_aslab, get_aslabs, update_aslab, delete_aslab
from apps.database import get_db

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: auth_service.OAuth2PasswordRequestForm = Depends()):
    return aslab_service.login(form_data)

@router.post("/create", response_model=dict)
def create_aslab_endpoint(aslab_data: dict, db: Session = Depends(get_db)):
    return create_aslab(db, aslab_data)

@router.get("/{nim}", response_model=dict)
def get_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    return get_aslab(db, nim)

@router.get("/", response_model=list)
def get_aslabs_endpoint(db: Session = Depends(get_db)):
    return get_aslabs(db)

@router.put("/{nim}", response_model=dict)
def update_aslab_endpoint(nim: str, aslab_data: dict, db: Session = Depends(get_db)):
    return update_aslab(db, nim, aslab_data)

@router.delete("/{nim}", response_model=dict)
def delete_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    return delete_aslab(db, nim)

