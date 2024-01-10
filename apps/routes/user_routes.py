from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.controllers.user_controller import *
from apps.database import get_db
from apps.helper.response import response
from apps.models.user import User

router = APIRouter()

@router.post('/create')
async def create_user_endpoint(user_data: dict, db: Session = Depends(get_db)):
    new_user = create_user(db, user_data)
    if not new_user:
        raise HTTPException(status_code=401, success=True, msg="User gagal dibuat", data=None)
    return response(status_code=200, success=True, msg="User berhasil dibuat", data=new_user)

@router.get('/{nim}')
async def get_user_endpoint(nim: str, db: Session = Depends(get_db)):
    user_detail = get_user(db, nim)
    if not user_detail:
        raise HTTPException(status_code=401, detail="Data User Tidak Ada")
    return response(status_code=200, success=True, msg="Data User ditemukan", data=user_detail)

@router.get('/')
async def get_users_endpoint(db: Session = Depends(get_db)):
    try:
        users_list = get_users(db)
        return response(status_code=200, success=True, msg="Data User ditemukan", data=users_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put('/{nim}')
async def update_user_endpoint(nim: str, user_data: dict, db: Session = Depends(get_db)):
    updated_user = update_user(db, nim, user_data)
    if not update_user:    
        raise HTTPException(status_code=400, detail='GAGAL')
    return response(status_code=200, success=True, msg="Data User berhasil diperbarui", data=updated_user)

@router.delete('/{nim}')
async def delete_user_endpoint(nim: str, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, nim)
    if not delete_user:    
        return HTTPException(status_code=200, detail="User gagal dihapus")
    return response(status_code=200, success=True, msg='Berhasil dihapus', data=deleted_user)
