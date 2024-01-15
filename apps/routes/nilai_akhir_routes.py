from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.nilai_akhir_controller import *
from apps.helper.response import response
from apps.schemas.nilai_akhir_schema import NilaiAkhirSchema

router = APIRouter()

@router.post("/")
async def create_nilai_akhir_endpoint(nilai_akhir_data: NilaiAkhirSchema, db: Session = Depends(get_db)):
    nilai = create_nilai_akhir(nilai_akhir_data, db)
    if nilai:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditambahkan!", data=nilai)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)


@router.get("/{usersid}/{kd_matkul}")
async def read_nilai_akhir_endpoint(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    nilai = get_nilai_akhir(usersid, kd_matkul, db)
    if nilai:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=nilai)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_nilai_akhir_endpoint(db: Session = Depends(get_db)):
    nilai = get_all_nilai_akhir(db)
    if nilai:
        try:
            return response(status_code=200, success=True, msg="Data berhasil ditemukan!", data=nilai)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{usersid}/{kd_matkul}")
async def update_nilai_akhir_endpoint(usersid: str, kd_matkul: str, nilai_akhir_data: NilaiAkhirSchema, db: Session = Depends(get_db)):
    nilai = update_nilai_akhir(nilai_akhir_data, usersid, kd_matkul, db)
    if nilai:
        try:
            return response(status_code=200, success=True, msg="Data berhasil diperbarui!", data=nilai)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{usersid}/{kd_matkul}")
async def delete_nilai_akhir_endpoint(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    nilai = delete_nilai_akhir(usersid, kd_matkul, db)
    if nilai:
        try:
            return response(status_code=200, success=True, msg="Data berhasil dihapus!", data=nilai)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
