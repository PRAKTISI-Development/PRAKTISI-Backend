from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.controllers import mata_kuliah_controller
# from apps.models.mata_kuliah import None
from apps.database import get_db
from apps.helper.response import response

router = APIRouter()


@router.get("/", response_model=None)
async def get_all_mata_kuliah(db: Session = Depends(get_db)):
    try:
        mata_kuliah_detail = mata_kuliah_controller.get_mata_kuliah(db)
        return response(status_code=200, success=True, msg="Data Mata Kuliah ditemukan", data=mata_kuliah_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{kode_matkul}", response_model=None)
async def get_mata_kuliah_by_code(kode_matkul: str, db: Session = Depends(get_db)):
    try:
        mata_kuliah_detail = mata_kuliah_controller.get_mata_kuliah_by_code(db, kode_matkul)
        return response(status_code=200, success=True, msg="Data Mata Kuliah ditemukan", data=mata_kuliah_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.post("/", response_model=None)
async def create_mata_kuliah(mata_kuliah_data: dict, db: Session = Depends(get_db)):
    try:
        new_mata_kuliah = mata_kuliah_controller.create_mata_kuliah(db, mata_kuliah_data)
        return response(status_code=201, success=True, msg="Mata Kuliah berhasil dibuat", data=new_mata_kuliah)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{kode_matkul}", response_model=None)
async def update_mata_kuliah(kode_matkul: str, mata_kuliah_data: dict, db: Session = Depends(get_db)):
    try:
        updated_mata_kuliah = mata_kuliah_controller.update_mata_kuliah(db, kode_matkul, mata_kuliah_data)
        return response(status_code=200, success=True, msg="Data Mata Kuliah berhasil diperbarui", data=updated_mata_kuliah)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{kode_matkul}", response_model=dict)
async def delete_mata_kuliah(kode_matkul: str, db: Session = Depends(get_db)):
    try:
        deleted_mata_kuliah = mata_kuliah_controller.delete_mata_kuliah(db, kode_matkul)
        return response(status_code=200, success=True, msg="Mata Kuliah berhasil dihapus", data=deleted_mata_kuliah)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
