from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.services import aslab_service, auth_service
from apps.models.aslab import Aslab
from apps.models.user import User
from apps.database import SessionLocal
from apps.services.aslab_service import *
from apps.database import get_db
from apps.helpers import response

router = APIRouter()

@router.post("/login", response_model=str)
async def login_for_access_token(form_data: auth_service.OAuth2PasswordBearer = Depends()):
    try:
        token = aslab_service.login(form_data)
        return response(status_code=200, success=True, msg="Login berhasil", data={"access_token": token})
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.post("/", response_model=dict)
async def create_aslab_endpoint(aslab_data: dict, db: Session = Depends(get_db)):
    try:
        new_aslab = create_aslab(db, aslab_data)
        return response(status_code=201, success=True, msg="Aslab berhasil dibuat", data=new_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{nim}", response_model=dict)
async def get_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        aslab_detail = get_aslab(db, nim)
        return response(status_code=200, success=True, msg="Data Aslab ditemukan", data=aslab_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_aslabs_endpoint(db: Session = Depends(get_db)):
    try:
        aslabs_list = get_aslabs(db)
        return response(status_code=200, success=True, msg="Data Aslab ditemukan", data=aslabs_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{nim}", response_model=dict)
async def update_aslab_endpoint(nim: str, aslab_data: dict, db: Session = Depends(get_db)):
    try:
        updated_aslab = update_aslab(db, nim, aslab_data)
        return response(status_code=200, success=True, msg="Data Aslab berhasil diperbarui", data=updated_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{nim}", response_model=dict)
async def delete_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        deleted_aslab = delete_aslab(db, nim)
        return response(status_code=200, success=True, msg="Aslab berhasil dihapus", data=deleted_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
