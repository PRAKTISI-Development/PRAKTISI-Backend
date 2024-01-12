from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.jadwal import Jadwal
from apps.database import get_db
from apps.controllers.jadwal_controller import *

router = APIRouter()

@router.post("/jadwal/", response_model=Jadwal)
def create_jadwal_endpoint(jadwal_data: Jadwal, db: Session = Depends(get_db)):
    return create_jadwal(jadwal_data, db)

@router.get("/jadwal/{kd_jadwal}", response_model=Jadwal)
def read_jadwal_endpoint(kd_jadwal: str, db: Session = Depends(get_db)):
    return get_jadwal(kd_jadwal, db)

@router.get("/jadwal/", response_model=list[Jadwal])
def read_all_jadwal_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_jadwal(skip, limit, db)

@router.put("/jadwal/{kd_jadwal}", response_model=Jadwal)
def update_jadwal_endpoint(kd_jadwal: str, jadwal_data: Jadwal, db: Session = Depends(get_db)):
    return update_jadwal(jadwal_data, kd_jadwal, db)

@router.delete("/jadwal/{kd_jadwal}", response_model=dict)
def delete_jadwal_endpoint(kd_jadwal: str, db: Session = Depends(get_db)):
    return delete_jadwal(kd_jadwal, db)
