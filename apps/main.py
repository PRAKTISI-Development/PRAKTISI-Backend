from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from apps.database import SessionLocal, engine
from apps.controllers import aslab_controller, praktikan_controller, jadwal_controller, mata_kuliah_controller, nilai_akhir_controller, tugas_controller, user_controller
from apps.models import Base

app = FastAPI()

# CORS middleware untuk mengizinkan permintaan dari semua origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Menggantilah tanda bintang dengan domain yang spesifik jika mungkin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi basis data
Base.metadata.create_all(bind=engine)

# Dependency untuk mendapatkan objek sesi basis data
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Menambahkan router untuk setiap controller
app.include_router(aslab_controller.router, prefix="/aslab", tags=["Aslab"])
app.include_router(praktikan_controller.router, prefix="/praktikan", tags=["Praktikan"])
app.include_router(jadwal_controller.router, prefix="/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_controller.router, prefix="/nilai_akhir", tags=["Nilai Akhir"])
app.include_router(tugas_controller.router, prefix="/tugas", tags=["Tugas"])
app.include_router(user_controller.router, prefix="/user", tags=["User"])
