from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.informasi_controller import *
from apps.schemas.informasi_schema import InformasiSchema

router = APIRouter()

@router.post("/", response_model=InformasiSchema)
def create_informasi_endpoint(request: Request, informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    informasi = create_informasi(request, informasi_data, db)
    return informasi

@router.get("/{kd_informasi}", response_model=None)
def read_informasi_endpoint(request: Request, kd_informasi: str, db: Session = Depends(get_db)):
    informasi = get_informasi(request, kd_informasi, db)
    return informasi

@router.get('/')
def read_all_informasi_endpoint(request: Request, db: Session = Depends(get_db)):
    informasi = get_all_informasi(request, db)
    return informasi

@router.put("/{kd_informasi}")
def update_informasi_endpoint(request: Request, kd_informasi: str, informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    informasi = update_informasi(request, informasi_data, kd_informasi, db)
    return informasi

@router.delete("/{kd_informasi}")
def delete_informasi_endpoint(request: Request, kd_informasi: str, db: Session = Depends(get_db)):
    informasi =  delete_informasi(request, kd_informasi, db)
    return informasi