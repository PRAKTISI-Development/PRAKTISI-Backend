from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.detail_pengumpulan_controller import *
from apps.schemas.detail_pengumpulan_schema import DetailPengumpulanSchema

router = APIRouter()

@router.post("/", response_model=DetailPengumpulanSchema)
async def create_detail_pengumpulan_endpoint(request: Request,detail_pengumpulan_data: DetailPengumpulanSchema=Depends(DetailPengumpulanSchema.as_form),db: Session = Depends(get_db)):
    return create_detail_pengumpulan(request, detail_pengumpulan_data, db)

@router.get("/{usersid}/{kd_tugas}")
async def read_detail_pengumpulan_endpoint(request:Request,usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    detail_pengumpulan = get_detail_pengumpulan(request, usersid, kd_tugas, db)
    return detail_pengumpulan

@router.get("/")
async def read_all_detail_pengumpulan_endpoint(request: Request, db: Session = Depends(get_db)):
    detail_pengumpulan = get_all_detail_pengumpulan(request, db)
    return detail_pengumpulan

@router.put("/{usersid}/{kd_tugas}")
async def update_detail_pengumpulan_endpoint(request: Request, usersid: str, kd_tugas: str, detail_pengumpulan_data: DetailPengumpulanSchema, db: Session = Depends(get_db)):
    return update_detail_pengumpulan(request, detail_pengumpulan_data, usersid, kd_tugas, db)

@router.delete("/{usersid}/{kd_tugas}")
async def delete_detail_pengumpulan_endpoint(request:Request, usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    return delete_detail_pengumpulan(request, usersid, kd_tugas, db)