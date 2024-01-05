from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.database import engine
from apps.controllers import aslab_controller, praktikan_controller, jadwal_controller, mata_kuliah_controller, nilai_akhir_controller, tugas_controller, user_controller
from apps.models import Base

app = FastAPI(
    title="REST-SERVER PRAKTISI",
    debug=True,
    version="1.0.0",
    description="PRAKTISI BACKEND APP",
    docs_url="/api_docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(aslab_controller.router, prefix="/aslab", tags=["Aslab"])
app.include_router(praktikan_controller.router, prefix="/praktikan", tags=["Praktikan"])
app.include_router(mata_kuliah_controller.router, prefix="/mata_kuliah", tags=["Jadwal"])
app.include_router(jadwal_controller.router, prefix="/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_controller.router, prefix="/nilai)akhir", tags=["Nilai Akhir"])
app.include_router(tugas_controller.router, prefix="/tugas", tags=["Tugas"])
app.include_router(user_controller.router, prefix="/user", tags=["User"])
