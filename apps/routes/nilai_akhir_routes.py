from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, Path

from apps.database import get_db
from apps.controllers.nilai_akhir_controller import *
from apps.schemas.nilai_akhir_schema import NilaiAkhirSchema

router = APIRouter()

@router.post("/")
async def create_nilai_akhir_endpoint(request: Request, nilai_akhir_data: NilaiAkhirSchema, db: Session = Depends(get_db)):
    return create_nilai_akhir(request, nilai_akhir_data, db)

@router.get("/{kd_matkul}")
async def read_akumulasi(request:Request, kd_matkul:str, db: Session = Depends(get_db)):
    return get_akumulasi(request, kd_matkul, db)

@router.get("/{kd_matkul}/download")
async def read_download_akumulasi(request:Request, kd_matkul:str, db: Session = Depends(get_db)):
    return get_download(request, kd_matkul, db)

@router.get("/{usersid}/{kd_matkul}")
async def read_nilai_akhir_endpoint(request: Request, usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    return get_nilai_akhir(request, usersid, kd_matkul, db)
    
@router.get("/")
async def read_all_nilai_akhir_endpoint(request: Request, db: Session = Depends(get_db)):
    return get_all_nilai_akhir(request, db)
    
@router.put("/{usersid}/{kd_matkul}")
async def update_nilai_akhir_endpoint(request: Request, nilai_akhir_data: NilaiAkhirSchema, usersid: str = Path(...), kd_matkul: str = Path(...), db: Session = Depends(get_db)):
    return update_nilai_akhir(request, nilai_akhir_data, usersid, kd_matkul, db)
    
@router.delete("/{usersid}/{kd_matkul}")
async def delete_nilai_akhir_endpoint(request: Request, usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    return delete_nilai_akhir(request, usersid, kd_matkul, db)