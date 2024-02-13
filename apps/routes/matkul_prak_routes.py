from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.matkul_prak_controller import *
from apps.schemas.matkul_prak_schema import MatkulPrakSchema

router = APIRouter()

@router.post("/", response_model=MatkulPrakSchema)
async def create_matkul_prak_endpoint(request: Request,matkul_prak_data: MatkulPrakSchema, db: Session = Depends(get_db)):
    matkul = create_matkul_prak(request, matkul_prak_data, db) 
    return matkul

@router.get("/{kd_matkul}", response_model=None)
async def read_matkul_prak_endpoint(request: Request, kd_matkul: str, db: Session = Depends(get_db)):
    matkul = get_matkul_prak(request, kd_matkul, db)
    return matkul

@router.get("/")
async def read_all_matkul_prak_endpoint(request: Request, db: Session = Depends(get_db)):
    matkul = get_all_matkul_prak(request, db)
    return matkul

@router.put("/{kd_matkul}")
async def update_matkul_prak_endpoint(request: Request, kd_matkul: str, matkul_prak_data: MatkulPrakSchema, db: Session = Depends(get_db)):
    matkul = update_matkul_prak(request, matkul_prak_data, kd_matkul, db)
    return matkul

@router.delete("/{kd_matkul}")
async def delete_matkul_prak_endpoint(request: Request, kd_matkul: str, db: Session = Depends(get_db)):
    matkul = delete_matkul_prak(request, kd_matkul, db)
    return matkul