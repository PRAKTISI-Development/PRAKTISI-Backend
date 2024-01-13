from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.models.jadwal import Jadwal
from apps.database import get_db
from apps.controllers.jadwal_controller import *
from apps.helper.response import response

router = APIRouter()

@router.post("/")
async def create_jadwal_endpoint(jadwal_data: Jadwal, db: Session = Depends(get_db)):
    jadwal = create_jadwal(jadwal_data, db)
    if jadwal:
        try:
            return response(status_code=200, success=True, msg="Jadwal berhasil ditambahkan!", data=jadwal)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kd_jadwal}")
async def read_jadwal_endpoint(kd_jadwal: str, db: Session = Depends(get_db)):
    jadwal = get_jadwal(kd_jadwal, db)
    if jadwal:
        try:
            return response(status_code=200, success=True, msg="Jadwal ditemukan!", data=jadwal)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_jadwal_endpoint(db: Session = Depends(get_db)):
    jadwal = get_all_jadwal(db)
    if jadwal:
        try:
            return response(status_code=200, success=True, msg="Jadwal berhasil ditemukan!", data=jadwal)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kd_jadwal}")
def update_jadwal_endpoint(kd_jadwal: str, jadwal_data: Jadwal, db: Session = Depends(get_db)):
    jadwal = update_jadwal(jadwal_data, kd_jadwal, db)
    if jadwal:
        try:
            return response(status_code=200, success=True, msg="Jadwal berhasil diperbarui!", data=jadwal)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
    
@router.delete("/{kd_jadwal}")
async def delete_jadwal_endpoint(kd_jadwal: str, db: Session = Depends(get_db)):
    jadwal = delete_jadwal(kd_jadwal, db)
    if jadwal:
        try:
            return response(status_code=200, success=True, msg="Jadwal berhasil dihapus!", data=jadwal)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
