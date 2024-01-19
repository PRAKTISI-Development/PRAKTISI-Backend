from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.informasi_controller import *
from apps.helpers.response import response
from apps.schemas.informasi_schema import InformasiSchema

router = APIRouter()

@router.post("/", response_model=InformasiSchema)
def create_informasi_endpoint(informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    informasi = create_informasi(informasi_data, db)
    if informasi:
        try:
            return response(status_code=200, success=True, msg="Informasi berhasil ditambahkan", data=informasi)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kd_informasi}", response_model=InformasiSchema)
async def read_informasi_endpoint(kd_informasi: str, db: Session = Depends(get_db)):
    informasi = get_informasi(kd_informasi, db)
    if informasi:
        try:
            return response(status_code=200, success=True, msg=f"Informasi {kd_informasi} ditemukan", data=informasi)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get('/')
async def read_all_informasi_endpoint(db: Session = Depends(get_db)):
    informasi = get_all_informasi(db)
    if informasi:
        try:
            return response(status_code=200, success=True, msg="Informasi ditemukan", data=informasi)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kd_informasi}")
async def update_informasi_endpoint(kd_informasi: str, informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    informasi = update_informasi(informasi_data, kd_informasi, db)
    if informasi:
        try:
            return response(status_code=200, success=True, msg="Informasi berhasil diperbarui!", data=informasi)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
        
@router.delete("/{kd_informasi}")
async def delete_informasi_endpoint(kd_informasi: str, db: Session = Depends(get_db)):
    informasi = delete_informasi(kd_informasi, db)
    if informasi:
        try:
            return response(status_code=200, success=True, msg="Informasi berhasil dihapus!", data=informasi)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
