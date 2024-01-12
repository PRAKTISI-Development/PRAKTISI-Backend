from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models.matkul_prak import MatkulPrakModel
from apps.database import get_db
from apps.controllers.matkul_prak_controller import (
    create_matkul_prak,
    get_matkul_prak,
    get_all_matkul_prak,
    update_matkul_prak,
    delete_matkul_prak,
)

router = APIRouter()

@router.post("/matkul_prak/", response_model=MatkulPrakModel)
def create_matkul_prak_endpoint(matkul_prak_data: MatkulPrakModel, db: Session = Depends(get_db)):
    return create_matkul_prak(matkul_prak_data, db)

@router.get("/matkul_prak/{kd_matkul}", response_model=MatkulPrakModel)
def read_matkul_prak_endpoint(kd_matkul: str, db: Session = Depends(get_db)):
    return get_matkul_prak(kd_matkul, db)

@router.get("/matkul_prak/", response_model=list[MatkulPrakModel])
def read_all_matkul_prak_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_matkul_prak(skip, limit, db)

@router.put("/matkul_prak/{kd_matkul}", response_model=MatkulPrakModel)
def update_matkul_prak_endpoint(kd_matkul: str, matkul_prak_data: MatkulPrakModel, db: Session = Depends(get_db)):
    return update_matkul_prak(matkul_prak_data, kd_matkul, db)

@router.delete("/matkul_prak/{kd_matkul}", response_model=dict)
def delete_matkul_prak_endpoint(kd_matkul: str, db: Session = Depends(get_db)):
    return delete_matkul_prak(kd_matkul, db)
