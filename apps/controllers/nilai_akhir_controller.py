from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.services.nilai_akhir_service import create_nilai_akhir, get_nilai_akhir, get_nilai_akhirs, update_nilai_akhir, delete_nilai_akhir
from apps.database import get_db

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_nilai_akhir_endpoint(nilai_akhir_data: dict, db: Session = Depends(get_db)):
    return create_nilai_akhir(db, nilai_akhir_data)

@router.get("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def get_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, db: Session = Depends(get_db)):
    return get_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul)

@router.get("/", response_model=list)
async def get_nilai_akhirs_endpoint(db: Session = Depends(get_db)):
    return get_nilai_akhirs(db)

@router.put("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def update_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, nilai_akhir_data: dict, db: Session = Depends(get_db)):
    return update_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul, nilai_akhir_data)

@router.delete("/{praktikan_nim}/{mata_kuliah_kode_matkul}", response_model=dict)
async def delete_nilai_akhir_endpoint(praktikan_nim: str, mata_kuliah_kode_matkul: str, db: Session = Depends(get_db)):
    return delete_nilai_akhir(db, praktikan_nim, mata_kuliah_kode_matkul)
