from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.tugas_controller import *
from apps.schemas.tugas_schema import TugasSchema

router = APIRouter()

@router.post("/", response_model=TugasSchema)
async def create_tugas_endpoint(request: Request, tugas_data: TugasSchema, db: Session = Depends(get_db)):
    tugas = create_tugas(request, tugas_data, db)
    return tugas

@router.get("/{kd_tugas}", response_model=None)
async def read_tugas_endpoint(request: Request, kd_tugas: str, db: Session = Depends(get_db)):
    tugas = get_tugas(request, kd_tugas, db)
    return tugas
    
@router.get("/")
async def read_all_tugas_endpoint(request: Request, db: Session = Depends(get_db)):
    tugas = get_all_tugas(request, db)
    return tugas

@router.put("/{kd_tugas}")
async def update_tugas_endpoint(request: Request, kd_tugas: str, tugas_data: TugasSchema, db: Session = Depends(get_db)):
    tugas = update_tugas(request, tugas_data, kd_tugas, db)
    return tugas

@router.delete("/{kd_tugas}", response_model=dict)
async def delete_tugas_endpoint(request:Request, kd_tugas: str, db: Session = Depends(get_db)):
    tugas = delete_tugas(request, kd_tugas, db)
    return tugas