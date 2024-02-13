from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, Path
from apps.database import get_db
from apps.controllers.nilai_akhir_controller import *
from apps.schemas.nilai_akhir_schema import NilaiAkhirSchema

router = APIRouter()

@router.post("/")
async def create_nilai_akhir_endpoint(request: Request, nilai_akhir_data: NilaiAkhirSchema, db: Session = Depends(get_db)):
    nilai_akhir = create_nilai_akhir(request, nilai_akhir_data, db)
    return nilai_akhir

@router.get("/{kd_matkul}")
async def read_akumulasi(request: Request, kd_matkul:str, db: Session = Depends(get_db)):
    akumulasi = get_akumulasi(request, kd_matkul, db)
    return akumulasi

@router.get("/{kd_matkul}/download")
async def read_download_akumulasi(request: Request, kd_matkul:str, db: Session = Depends(get_db)):
    files = get_download(request, kd_matkul, db)
    return files

@router.get("/{usersid}/{kd_matkul}")
async def read_nilai_akhir_endpoint(request: Request, usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    nilai_akhir = get_nilai_akhir(request, usersid, kd_matkul, db)
    return nilai_akhir
    
@router.get("/")
async def read_all_nilai_akhir_endpoint(request: Request, db: Session = Depends(get_db)):
    nilai_akhir = get_all_nilai_akhir(request, db)
    return nilai_akhir
    
@router.put("/{usersid}/{kd_matkul}")
async def update_nilai_akhir_endpoint(request: Request, nilai_akhir_data: NilaiAkhirSchema, usersid: str = Path(...), kd_matkul: str = Path(...), db: Session = Depends(get_db)):
    nilai_akhir = update_nilai_akhir(request, nilai_akhir_data, usersid, kd_matkul, db)
    return nilai_akhir
    
@router.delete("/{usersid}/{kd_matkul}")
async def delete_nilai_akhir_endpoint(request: Request, usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    nilai_akhir = delete_nilai_akhir(request, usersid, kd_matkul, db)
    return nilai_akhir