from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services import mata_kuliah_service
from apps.models.mata_kuliah import MataKuliah
from apps.database import get_db

router = APIRouter()

@router.get("/", response_model=List[MataKuliah])
async def get_all_mata_kuliah(db: Session = Depends(get_db)):
    return mata_kuliah_service.get_mata_kuliah(db)

@router.get("/{kode_matkul}", response_model=MataKuliah)
async def get_mata_kuliah_by_code(kode_matkul: str, db: Session = Depends(get_db)):
    return mata_kuliah_service.get_mata_kuliah_by_code(db, kode_matkul)

@router.post("/", response_model=MataKuliah)
async def create_mata_kuliah(mata_kuliah_data: dict, db: Session = Depends(get_db)):
    return mata_kuliah_service.create_mata_kuliah(db, mata_kuliah_data)

@router.put("/{kode_matkul}", response_model=MataKuliah)
async def update_mata_kuliah(kode_matkul: str, mata_kuliah_data: dict, db: Session = Depends(get_db)):
    return mata_kuliah_service.update_mata_kuliah(db, kode_matkul, mata_kuliah_data)

@router.delete("/{kode_matkul}", response_model=dict)
async def delete_mata_kuliah(kode_matkul: str, db: Session = Depends(get_db)):
    return mata_kuliah_service.delete_mata_kuliah(db, kode_matkul)
