from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.controllers.praktikan_controller import *
from apps.database import get_db
from apps.helper.response import response

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_praktikan_endpoint(praktikan_data: dict, db: Session = Depends(get_db)):
    try:
        new_praktikan = create_praktikan(db, praktikan_data)
        return response(status_code=201, success=True, msg="Praktikan berhasil dibuat", data=new_praktikan)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_praktikans_endpoint(db: Session = Depends(get_db)):
    try:
        praktikans_list = get_praktikans(db)
        return response(status_code=200, success=True, msg="Data Praktikan ditemukan", data=praktikans_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{nim}", response_model=dict)
async def get_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        praktikan_detail = get_praktikan(db, nim)
        return response(status_code=200, success=True, msg="Data Praktikan ditemukan", data=praktikan_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)


@router.put("/{nim}", response_model=dict)
async def update_praktikan_endpoint(nim: str, praktikan_data: dict, db: Session = Depends(get_db)):
    try:
        updated_praktikan = update_praktikan(db, nim, praktikan_data)
        return response(status_code=200, success=True, msg="Data Praktikan berhasil diperbarui", data=updated_praktikan)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{nim}", response_model=dict)
async def delete_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        deleted_praktikan = delete_praktikan(db, nim)
        return response(status_code=200, success=True, msg="Praktikan berhasil dihapus", data=deleted_praktikan)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
