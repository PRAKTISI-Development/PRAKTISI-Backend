from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.user_service import *
from apps.database import get_db
from apps.helpers import response

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_user_endpoint(user_data: dict, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_data)
        return response(status_code=201, success=True, msg="User berhasil dibuat", data=new_user)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{nim}", response_model=dict)
async def get_user_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        user_detail = get_user(db, nim)
        return response(status_code=200, success=True, msg="Data User ditemukan", data=user_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_users_endpoint(db: Session = Depends(get_db)):
    try:
        users_list = get_users(db)
        return response(status_code=200, success=True, msg="Data User ditemukan", data=users_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{nim}", response_model=dict)
async def update_user_endpoint(nim: str, user_data: dict, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db, nim, user_data)
        return response(status_code=200, success=True, msg="Data User berhasil diperbarui", data=updated_user)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{nim}", response_model=dict)
async def delete_user_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        deleted_user = delete_user(db, nim)
        return response(status_code=200, success=True, msg="User berhasil dihapus", data=deleted_user)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
