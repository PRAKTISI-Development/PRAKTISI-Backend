from fastapi import APIRouter, Request, Depends, Path
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.kehadiran_controller import *
from apps.schemas.kehadiran_schema import KehadiranSchema

router = APIRouter()

@router.post("/")
async def create_kehadiran_endpoint(request: Request, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db)):
    kehadiran = create_kehadiran(request, kehadiran_data, db)
    return kehadiran

@router.get("/{usersid}/{kd_jadwal}")
async def read_kehadiran_endpoint(request: Request, usersid: str, kd_jadwal: str, db: Session = Depends(get_db)):
    kehadiran = get_kehadiran(request, usersid, kd_jadwal, db)
    return kehadiran

@router.get("/")
async def read_all_kehadiran_endpoint(request: Request, db: Session = Depends(get_db) ):
    kehadiran = get_all_kehadiran(request, db)
    return kehadiran

@router.put("/{usersid}/{kd_jadwal}")
async def update_kehadiran_endpoint(request: Request, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db), usersid: str= Path(...), kd_jadwal: str= Path(...)):
    kehadiran = update_kehadiran(request, kehadiran_data, usersid, kd_jadwal, db)
    return kehadiran

@router.delete("/{usersid}/{kd_jadwal}")
async def delete_kehadiran_endpoint(request: Request, usersid: str, kd_jadwal: str, db: Session = Depends(get_db)):
    jadwal = delete_kehadiran(request, usersid, kd_jadwal, db)
    return jadwal