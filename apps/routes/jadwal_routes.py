from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.jadwal_controller import *
from apps.schemas.jadwal_schema import JadwalSchema

router = APIRouter()

@router.post("/", response_model=JadwalSchema)
async def create_jadwal_endpoint(request: Request,jadwal_data: JadwalSchema, db: Session = Depends(get_db)):
    return create_jadwal(request, jadwal_data, db)

@router.get("/{kd_jadwal}")
async def read_jadwal_endpoint(request: Request,kd_jadwal: str, db: Session = Depends(get_db)):
    return get_jadwal(request, kd_jadwal, db)

@router.get("/")
async def read_all_jadwal_endpoint(request: Request,db: Session = Depends(get_db)):
    return get_all_jadwal(request, db)
    
@router.put("/{kd_jadwal}")
def update_jadwal_endpoint(request: Request,kd_jadwal: str, jadwal_data: JadwalSchema, db: Session = Depends(get_db)):
    return update_jadwal(request, jadwal_data, kd_jadwal, db)
    
@router.delete("/{kd_jadwal}")
async def delete_jadwal_endpoint(request: Request,kd_jadwal: str, db: Session = Depends(get_db)):
    return delete_jadwal(request, kd_jadwal, db)