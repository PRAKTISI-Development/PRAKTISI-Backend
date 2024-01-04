from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.tugas_service import create_tugas, get_tugas, get_tugass, update_tugas, delete_tugas
from apps.database import get_db

router = APIRouter()

@router.post("/create", response_model=dict)
def create_tugas_endpoint(tugas_data: dict, db: Session = Depends(get_db)):
    return create_tugas(db, tugas_data)

@router.get("/{kode_tugas}", response_model=dict)
def get_tugas_endpoint(kode_tugas: str, db: Session = Depends(get_db)):
    return get_tugas(db, kode_tugas)

@router.get("/", response_model=list)
def get_tugass_endpoint(db: Session = Depends(get_db)):
    return get_tugass(db)

@router.put("/{kode_tugas}", response_model=dict)
def update_tugas_endpoint(kode_tugas: str, tugas_data: dict, db: Session = Depends(get_db)):
    return update_tugas(db, kode_tugas, tugas_data)

@router.delete("/{kode_tugas}", response_model=dict)
def delete_tugas_endpoint(kode_tugas: str, db: Session = Depends(get_db)):
    return delete_tugas(db, kode_tugas)
