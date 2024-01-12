from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.detail_pengumpulan import DetailPengumpulan as DetailPengumpulanModel
from apps.database import get_db
from apps.controllers import (
    create_detail_pengumpulan,
    get_detail_pengumpulan,
    get_all_detail_pengumpulan,
    update_detail_pengumpulan,
    delete_detail_pengumpulan,
)

router = APIRouter()

@router.post("/detail_pengumpulan/", response_model=DetailPengumpulanModel)
def create_detail_pengumpulan_endpoint(detail_pengumpulan_data: DetailPengumpulanModel, db: Session = Depends(get_db)):
    return create_detail_pengumpulan(detail_pengumpulan_data, db)

@router.get("/detail_pengumpulan/{usersid}/{kd_tugas}", response_model=DetailPengumpulanModel)
def read_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    return get_detail_pengumpulan(usersid, kd_tugas, db)

@router.get("/detail_pengumpulan/", response_model=list[DetailPengumpulanModel])
def read_all_detail_pengumpulan_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_detail_pengumpulan(skip, limit, db)

@router.put("/detail_pengumpulan/{usersid}/{kd_tugas}", response_model=DetailPengumpulanModel)
def update_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, detail_pengumpulan_data: DetailPengumpulanModel, db: Session = Depends(get_db)):
    return update_detail_pengumpulan(detail_pengumpulan_data, usersid, kd_tugas, db)

@router.delete("/detail_pengumpulan/{usersid}/{kd_tugas}", response_model=dict)
def delete_detail_pengumpulan_endpoint(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    return delete_detail_pengumpulan(usersid, kd_tugas, db)
