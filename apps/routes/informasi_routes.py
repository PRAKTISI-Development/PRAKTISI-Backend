from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.informasi import Informasi
from apps.database import get_db
from apps.controllers.informasi_controller import (
    create_informasi,
    get_informasi,
    get_all_informasi,
    update_informasi,
    delete_informasi,
)

router = APIRouter()

@router.post("/informasi/", response_model=InformasiModel)
def create_informasi_endpoint(informasi_data: InformasiModel, db: Session = Depends(get_db)):
    return create_informasi(informasi_data, db)

@router.get("/informasi/{kd_informasi}", response_model=InformasiModel)
def read_informasi_endpoint(kd_informasi: str, db: Session = Depends(get_db)):
    return get_informasi(kd_informasi, db)

@router.get("/informasi/", response_model=list[InformasiModel])
def read_all_informasi_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_informasi(skip, limit, db)

@router.put("/informasi/{kd_informasi}", response_model=InformasiModel)
def update_informasi_endpoint(kd_informasi: str, informasi_data: InformasiModel, db: Session = Depends(get_db)):
    return update_informasi(informasi_data, kd_informasi, db)

@router.delete("/informasi/{kd_informasi}", response_model=dict)
def delete_informasi_endpoint(kd_informasi: str, db: Session = Depends(get_db)):
    return delete_informasi(kd_informasi, db)
