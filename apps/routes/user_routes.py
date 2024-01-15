from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.users_controller import *
from apps.helper.response import response
from apps.schemas.user_schema import UserSchema

router = APIRouter()

@router.post("/", response_model=None)
async def create_user_endpoint(user_data: UserSchema, db: Session = Depends(get_db)):
    user = create_user(user_data, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="User berhasil ditambahkan!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{userid}", response_model=None)
async def read_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = get_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="User berhasil ditemukan!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=None)
async def read_all_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(skip, limit, db)
    if users:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil ditemukan!", data=users)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{userid}", response_model=None)
async def update_user_endpoint(userid: str, user_data: UserSchema, db: Session = Depends(get_db)):
    user = update_user(user_data, userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil diperbarui!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{userid}", response_model=None)
async def delete_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = delete_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil dihapus!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
