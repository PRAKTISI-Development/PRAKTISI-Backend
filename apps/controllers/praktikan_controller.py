from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.praktikan_service import create_praktikan, get_praktikan, get_praktikans, update_praktikan, delete_praktikan
from apps.database import get_db

router = APIRouter()

@router.post("/create", response_model=dict)
def create_praktikan_endpoint(praktikan_data: dict, db: Session = Depends(get_db)):
    return create_praktikan(db, praktikan_data)

@router.get("/{nim}", response_model=dict)
def get_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    return get_praktikan(db, nim)

@router.get("/", response_model=list)
def get_praktikans_endpoint(db: Session = Depends(get_db)):
    return get_praktikans(db)

@router.put("/{nim}", response_model=dict)
def update_praktikan_endpoint(nim: str, praktikan_data: dict, db: Session = Depends(get_db)):
    return update_praktikan(db, nim, praktikan_data)

@router.delete("/{nim}", response_model=dict)
def delete_praktikan_endpoint(nim: str, db: Session = Depends(get_db)):
    return delete_praktikan(db, nim)
