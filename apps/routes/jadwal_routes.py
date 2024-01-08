from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.controllers.jadwal_controller import *
from apps.database import get_db
from apps.helper.response import response

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_jadwal_endpoint(jadwal_data: dict, db: Session = Depends(get_db)):
    try:
        new_jadwal = create_jadwal(db, jadwal_data)
        return response(status_code=201, success=True, msg="Jadwal berhasil dibuat", data=new_jadwal)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kode_jadwal}", response_model=dict)
async def get_jadwal_endpoint(kode_jadwal: str, db: Session = Depends(get_db)):
    try:
        jadwal_detail = get_jadwal(db, kode_jadwal)
        return response(status_code=200, success=True, msg="Data Jadwal ditemukan", data=jadwal_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_jadwals_endpoint(db: Session = Depends(get_db)):
    try:
        jadwals_list = get_jadwals(db)
        return response(status_code=200, success=True, msg="Data Jadwal ditemukan", data=jadwals_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kode_jadwal}", response_model=dict)
async def update_jadwal_endpoint(kode_jadwal: str, jadwal_data: dict, db: Session = Depends(get_db)):
    try:
        updated_jadwal = update_jadwal(db, kode_jadwal, jadwal_data)
        return response(status_code=200, success=True, msg="Data Jadwal berhasil diperbarui", data=updated_jadwal)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{kode_jadwal}", response_model=dict)
async def delete_jadwal_endpoint(kode_jadwal: str, db: Session = Depends(get_db)):
    try:
        deleted_jadwal = delete_jadwal(db, kode_jadwal)
        return response(status_code=200, success=True, msg="Jadwal berhasil dihapus", data=deleted_jadwal)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
