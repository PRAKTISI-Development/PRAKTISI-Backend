from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.jadwal_service import create_jadwal, get_jadwal, get_jadwals, update_jadwal, delete_jadwal
from apps.database import get_db

router = APIRouter()

@router.post("/create", response_model=dict)
def create_jadwal_endpoint(jadwal_data: dict, db: Session = Depends(get_db)):
    return create_jadwal(db, jadwal_data)

@router.get("/{kode_jadwal}", response_model=dict)
def get_jadwal_endpoint(kode_jadwal: str, db: Session = Depends(get_db)):
    return get_jadwal(db, kode_jadwal)

@router.get("/", response_model=list)
def get_jadwals_endpoint(db: Session = Depends(get_db)):
    return get_jadwals(db)

@router.put("/{kode_jadwal}", response_model=dict)
def update_jadwal_endpoint(kode_jadwal: str, jadwal_data: dict, db: Session = Depends(get_db)):
    return update_jadwal(db, kode_jadwal, jadwal_data)

@router.delete("/{kode_jadwal}", response_model=dict)
def delete_jadwal_endpoint(kode_jadwal: str, db: Session = Depends(get_db)):
    return delete_jadwal(db, kode_jadwal)
