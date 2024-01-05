from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.tugas_service import *
from apps.database import get_db
from apps.helpers import response

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_tugas_endpoint(tugas_data: dict, db: Session = Depends(get_db)):
    try:
        new_tugas = create_tugas(db, tugas_data)
        return response(status_code=201, success=True, msg="Tugas berhasil dibuat", data=new_tugas)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kode_tugas}", response_model=dict)
async def get_tugas_endpoint(kode_tugas: str, db: Session = Depends(get_db)):
    try:
        tugas_detail = get_tugas(db, kode_tugas)
        return response(status_code=200, success=True, msg="Data Tugas ditemukan", data=tugas_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_tugass_endpoint(db: Session = Depends(get_db)):
    try:
        tugass_list = get_tugass(db)
        return response(status_code=200, success=True, msg="Data Tugas ditemukan", data=tugass_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kode_tugas}", response_model=dict)
async def update_tugas_endpoint(kode_tugas: str, tugas_data: dict, db: Session = Depends(get_db)):
    try:
        updated_tugas = update_tugas(db, kode_tugas, tugas_data)
        return response(status_code=200, success=True, msg="Data Tugas berhasil diperbarui", data=updated_tugas)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{kode_tugas}", response_model=dict)
async def delete_tugas_endpoint(kode_tugas: str, db: Session = Depends(get_db)):
    try:
        deleted_tugas = delete_tugas(db, kode_tugas)
        return response(status_code=200, success=True, msg="Tugas berhasil dihapus", data=deleted_tugas)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
