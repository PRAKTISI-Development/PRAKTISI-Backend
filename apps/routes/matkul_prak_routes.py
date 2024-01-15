from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.matkul_prak_controller import *
from apps.helpers.response import response
from apps.schemas.matkul_prak_schema import MatkulPrakSchema

router = APIRouter()

@router.post("/")
async def create_matkul_prak_endpoint(matkul_prak_data: MatkulPrakSchema, db: Session = Depends(get_db)):
    matkul = create_matkul_prak(matkul_prak_data, db)
    if matkul:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditambahkan!", data=matkul)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kd_matkul}")
async def read_matkul_prak_endpoint(kd_matkul: str, db: Session = Depends(get_db)):
    matkul = get_matkul_prak(kd_matkul, db)
    if matkul:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=matkul)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_matkul_prak_endpoint(db: Session = Depends(get_db)):
    matkul = get_all_matkul_prak(db)
    if matkul:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=matkul)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kd_matkul}")
async def update_matkul_prak_endpoint(kd_matkul: str, matkul_prak_data: MatkulPrakSchema, db: Session = Depends(get_db)):
    matkul = update_matkul_prak(matkul_prak_data, kd_matkul, db)
    if matkul:
        try:
            return response(status_code=200, success=True, msg="Data berhasil diperbarui!", data=matkul)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{kd_matkul}")
async def delete_matkul_prak_endpoint(kd_matkul: str, db: Session = Depends(get_db)):
    matkul = delete_matkul_prak(kd_matkul, db)
    if matkul:
        try:
            return response(status_code=200, success=True, msg="Data berhasil dihapus!", data=matkul)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
