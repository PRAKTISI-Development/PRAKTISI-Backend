from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.kehadiran import KehadiranModel
from apps.database import get_db
from apps.controllers import (
    create_kehadiran,
    get_kehadiran,
    get_all_kehadiran,
    update_kehadiran,
    delete_kehadiran,
)

router = APIRouter()

@router.post("/kehadiran/", response_model=KehadiranModel)
def create_kehadiran_endpoint(kehadiran_data: KehadiranModel, db: Session = Depends(get_db)):
    return create_kehadiran(kehadiran_data, db)

@router.get("/kehadiran/{usersid}/{kd_matkul}/{pertemuan}", response_model=KehadiranModel)
def read_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    return get_kehadiran(usersid, kd_matkul, pertemuan, db)

@router.get("/kehadiran/", response_model=list[KehadiranModel])
def read_all_kehadiran_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_kehadiran(skip, limit, db)

@router.put("/kehadiran/{usersid}/{kd_matkul}/{pertemuan}", response_model=KehadiranModel)
def update_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, kehadiran_data: KehadiranModel, db: Session = Depends(get_db)):
    return update_kehadiran(kehadiran_data, usersid, kd_matkul, pertemuan, db)

@router.delete("/kehadiran/{usersid}/{kd_matkul}/{pertemuan}", response_model=dict)
def delete_kehadiran_endpoint(usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    return delete_kehadiran(usersid, kd_matkul, pertemuan, db)
