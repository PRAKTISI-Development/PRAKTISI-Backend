from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.tugas import Tugas
from apps.database import get_db
from apps.controllers import (
    create_tugas,
    get_tugas,
    get_all_tugas,
    update_tugas,
    delete_tugas,
)

router = APIRouter()

@router.post("/tugas/", response_model=Tugas)
def create_tugas_endpoint(tugas_data: Tugas, db: Session = Depends(get_db)):
    return create_tugas(tugas_data, db)

@router.get("/tugas/{kd_tugas}", response_model=Tugas)
def read_tugas_endpoint(kd_tugas: str, db: Session = Depends(get_db)):
    return get_tugas(kd_tugas, db)

@router.get("/tugas/", response_model=list[Tugas])
def read_all_tugas_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_tugas(skip, limit, db)

@router.put("/tugas/{kd_tugas}", response_model=Tugas)
def update_tugas_endpoint(kd_tugas: str, tugas_data: Tugas, db: Session = Depends(get_db)):
    return update_tugas(tugas_data, kd_tugas, db)

@router.delete("/tugas/{kd_tugas}", response_model=dict)
def delete_tugas_endpoint(kd_tugas: str, db: Session = Depends(get_db)):
    return delete_tugas(kd_tugas, db)
