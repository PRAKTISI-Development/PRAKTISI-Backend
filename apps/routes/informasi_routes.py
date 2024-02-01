from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.informasi_controller import *
from apps.schemas.informasi_schema import InformasiSchema

router = APIRouter()

@router.post("/", response_model=InformasiSchema)
def create_informasi_endpoint(request: Request, informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    return create_informasi(request, informasi_data, db)

@router.get("/{kd_informasi}", response_model=None)
def read_informasi_endpoint(request: Request, kd_informasi: str, db: Session = Depends(get_db)):
    return get_informasi(request, kd_informasi, db)

@router.get('/')
def read_all_informasi_endpoint(request: Request, db: Session = Depends(get_db)):
    return get_all_informasi(request, db)

@router.put("/{kd_informasi}")
def update_informasi_endpoint(request: Request, kd_informasi: str, informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    return update_informasi(request, informasi_data, kd_informasi, db)

@router.delete("/{kd_informasi}")
def delete_informasi_endpoint(request: Request, kd_informasi: str, db: Session = Depends(get_db)):
    return delete_informasi(request, kd_informasi, db)