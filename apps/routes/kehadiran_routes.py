from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.kehadiran_controller import *
from apps.helpers.response import response
from apps.schemas.kehadiran_schema import KehadiranSchema

router = APIRouter()

@router.post("/")
async def create_kehadiran_endpoint(request:Request, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db)):
    kehadiran = create_kehadiran(request, kehadiran_data, db)
    if kehadiran:
        try:
            return response(request, status_code=200, success=True, msg="User dinyatakan hadir!", data=kehadiran)
        except HTTPException as e:
            return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{usersid}/{kd_matkul}/{pertemuan}")
async def read_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    kehadiran = get_kehadiran(usersid, kd_matkul, pertemuan, db)
    if kehadiran:
        try:
            return response(status_code=200, success=True, msg="Data kehadiran ditemukan!", data=kehadiran)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_kehadiran_endpoint(request:Request, db: Session = Depends(get_db) ):
    kehadiran = get_all_kehadiran(db)
    if kehadiran:
        try:
            return response(request, status_code=200, success=True, msg="Data kehadiran ditemukan!", data=kehadiran)
        except HTTPException as e:
            return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{usersid}/{kd_matkul}/{pertemuan}")
async def update_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db)):
    kehadiran = update_kehadiran(kehadiran_data, usersid, kd_matkul, pertemuan, db)
    if kehadiran:
        try:
            return response(status_code=200, success=True, msg="Data berhasil diperbarui!", data=kehadiran)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{usersid}/{kd_matkul}/{pertemuan}")
async def delete_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    kehadiran = delete_kehadiran(usersid, kd_matkul, pertemuan, db)
    if kehadiran:
        try:
            return response(status_code=200, success=True, msg="Data berhasil dihapus!", data=kehadiran)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
