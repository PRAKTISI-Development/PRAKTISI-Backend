from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.detail_pengumpulan import DetailPengumpulan as DetailPengumpulanModel
from apps.database import get_db
from apps.controllers.detail_pengumpulan_controller import *
from apps.helper.response import response

router = APIRouter()

@router.post("/")
async def create_detail_pengumpulan_endpoint(detail_pengumpulan_data: DetailPengumpulanModel, db: Session = Depends(get_db)):
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
async def read_all_detail_pengumpulan_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    detail_pengumpulan = get_all_detail_pengumpulan(skip, limit, db)
    if detail_pengumpulan:
        try:
            return response(status_code=200, success=True, msg="Data ditemukan!", data=detail_pengumpulan)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{usersid}/{kd_tugas}")
async def update_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, detail_pengumpulan_data: DetailPengumpulanModel, db: Session = Depends(get_db)):
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


