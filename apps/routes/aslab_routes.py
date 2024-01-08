from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.aslab import Aslab
from apps.controllers.aslab_controller import *
from apps.database import get_db
from apps.helper.response import response

router = APIRouter()

@router.post("/", response_model=dict)
async def create_aslab_endpoint(aslab_data: dict, db: Session = Depends(get_db)):
    try:
        new_aslab = create_aslab(db, aslab_data)
        return response(status_code=201, success=True, msg="Aslab berhasil dibuat", data=new_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{nim}", response_model=list)
async def get_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        # aslab_detail = get_aslab(db, nim)
        aslab_detail = {
            'nama' : 'Wahyu Kesuma Bakti',
            'nim'  : nim
        }
        return response(status_code=200, success=True, msg="Data Aslab ditemukan", data=aslab_detail)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=list)
async def get_aslabs_endpoint(db: Session = Depends(get_db)):
    try:
        aslabs_list = get_aslabs(db)
        return response(status_code=200, success=True, msg="Data Aslab ditemukan", data=aslabs_list)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{nim}", response_model=dict)
async def update_aslab_endpoint(nim: str, aslab_data: dict, db: Session = Depends(get_db)):
    try:
        updated_aslab = update_aslab(db, nim, aslab_data)
        return response(status_code=200, success=True, msg="Data Aslab berhasil diperbarui", data=updated_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{nim}", response_model=dict)
async def delete_aslab_endpoint(nim: str, db: Session = Depends(get_db)):
    try:
        deleted_aslab = delete_aslab(db, nim)
        return response(status_code=200, success=True, msg="Aslab berhasil dihapus", data=deleted_aslab)
    except HTTPException as e:
        return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
