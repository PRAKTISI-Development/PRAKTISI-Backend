from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.controllers.nilai_akhir_controller import *
from apps.database import get_db
from apps.helper import response

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_nilai_akhir_endpoint(nilai_akhir_data: dict, db: Session = Depends(get_db)):
    try:
        new_nilai_akhir = create_nilai_akhir(db, nilai_akhir_data)
        return response(status_code=201, success=True, msg="Nilai Akhir berhasil dibuat", data=new_nilai_akhir)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def get_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, db: Session = Depends(get_db)):
    try:
        nilai_akhir_detail = get_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul)
        return response(status_code=200, success=True, msg="Data Nilai Akhir ditemukan", data=nilai_akhir_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_nilai_akhirs_endpoint(db: Session = Depends(get_db)):
    try:
        nilai_akhirs_list = get_nilai_akhirs(db)
        return response(status_code=200, success=True, msg="Data Nilai Akhir ditemukan", data=nilai_akhirs_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def update_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, nilai_akhir_data: dict, db: Session = Depends(get_db)):
    try:
        updated_nilai_akhir = update_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul, nilai_akhir_data)
        return response(status_code=200, success=True, msg="Data Nilai Akhir berhasil diperbarui", data=updated_nilai_akhir)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def delete_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, db: Session = Depends(get_db)):
    try:
        deleted_nilai_akhir = delete_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul)
        return response(status_code=200, success=True, msg="Nilai Akhir berhasil dihapus", data=deleted_nilai_akhir)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
