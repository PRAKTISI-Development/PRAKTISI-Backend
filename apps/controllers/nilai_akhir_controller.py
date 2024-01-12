from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.nilai_akhir import NilaiAkhirModel
from apps.database import get_db
from apps.controllers.nilai_akhir_controller import (
    create_nilai_akhir,
    get_nilai_akhir,
    get_all_nilai_akhir,
    update_nilai_akhir,
    delete_nilai_akhir,
)

router = APIRouter()

@router.post("/nilai_akhir/", response_model=NilaiAkhirModel)
def create_nilai_akhir_endpoint(nilai_akhir_data: NilaiAkhirModel, db: Session = Depends(get_db)):
    return create_nilai_akhir(nilai_akhir_data, db)

@router.get("/nilai_akhir/{usersid}/{kd_matkul}", response_model=NilaiAkhirModel)
def read_nilai_akhir_endpoint(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    return get_nilai_akhir(usersid, kd_matkul, db)

@router.get("/nilai_akhir/", response_model=list[NilaiAkhirModel])
def read_all_nilai_akhir_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_nilai_akhir(skip, limit, db)

@router.put("/nilai_akhir/{usersid}/{kd_matkul}", response_model=NilaiAkhirModel)
def update_nilai_akhir_endpoint(usersid: str, kd_matkul: str, nilai_akhir_data: NilaiAkhirModel, db: Session = Depends(get_db)):
    return update_nilai_akhir(nilai_akhir_data, usersid, kd_matkul, db)

@router.delete("/nilai_akhir/{usersid}/{kd_matkul}", response_model=dict)
def delete_nilai_akhir_endpoint(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    return delete_nilai_akhir(usersid, kd_matkul, db)
