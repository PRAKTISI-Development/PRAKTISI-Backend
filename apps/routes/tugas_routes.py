from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.tugas_controller import *
from apps.helper.response import response
from apps.schemas.tugas_schema import TugasSchema


router = APIRouter()

@router.post("/")
async def create_tugas_endpoint(tugas_data: TugasSchema, db: Session = Depends(get_db)):
    tugas = create_tugas(tugas_data, db)
    if tugas:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditambahkan!", data=tugas)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kd_tugas}")
async def read_tugas_endpoint(kd_tugas: str, db: Session = Depends(get_db)):
    tugas = get_tugas(kd_tugas, db)
    if tugas:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=tugas)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_tugas_endpoint( db: Session = Depends(get_db)):
    tugas = get_tugas(db)
    if tugas:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=tugas)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)


@router.put("/{kd_tugas}")
async def update_tugas_endpoint(kd_tugas: str, tugas_data: TugasSchema, db: Session = Depends(get_db)):
    tugas = update_tugas(tugas_data, kd_tugas, db)
    if tugas:
        try:
            return response(status_code=200, success=True, msg="Data berhasil diperbarui!", data=tugas)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{kd_tugas}", response_model=dict)
async def delete_tugas_endpoint(kd_tugas: str, db: Session = Depends(get_db)):
    tugas = delete_tugas(kd_tugas, db)
    if tugas:
        try:
            return response(status_code=200, success=True, msg="Data berhasil dihapus!", data=tugas)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

