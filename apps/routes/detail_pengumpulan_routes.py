from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.detail_pengumpulan_controller import *
from apps.helpers.response import response
from apps.schemas.detail_pengumpulan_schema import DetailPengumpulanSchema

router = APIRouter()

@router.post("/", response_model=DetailPengumpulanSchema)
async def create_detail_pengumpulan_endpoint(detail_pengumpulan_data: DetailPengumpulanSchema, db: Session = Depends(get_db)):
    detail_pengumpulan = create_detail_pengumpulan(detail_pengumpulan_data, db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg="Berhasil ditambahkan", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{usersid}/{kd_tugas}")
async def read_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    detail_pengumpulan = get_detail_pengumpulan(usersid, kd_tugas, db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg=f"Data {usersid} ditemukan!", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/")
async def read_all_detail_pengumpulan_endpoint(db: Session = Depends(get_db)):
    detail_pengumpulan = get_all_detail_pengumpulan(db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg="Data ditemukan!", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{usersid}/{kd_tugas}")
async def update_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, detail_pengumpulan_data: DetailPengumpulanSchema, db: Session = Depends(get_db)):
    detail_pengumpulan = update_detail_pengumpulan(detail_pengumpulan_data, usersid, kd_tugas, db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg="Data ditemukan!", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{usersid}/{kd_tugas}")
async def delete_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    detail_pengumpulan = delete_detail_pengumpulan(usersid, kd_tugas, db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg="Data berhasil dihapus!", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)


