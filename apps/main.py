from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from apps.database import Base, engine
from apps.routes import *

app = FastAPI(
    title="REST SERVER PRAKTISI",
    debug=False,
    version="1.0.0",
    description="PRAKTISI Backend Web Application",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get('/')
def root():
    return RedirectResponse(url='/redocs', status_code=303)

Base.metadata.create_all(bind=engine)
app.include_router(detail_pengumpulan_routes.router, prefix="/v1/detail_pengumpulan", tags=["Detail Pengumpulan"])
app.include_router(kehadiran_routes.router, prefix="/v1/kehadiran", tags=["Kehadiran"])
app.include_router(informasi_routes.router, prefix="/v1/informasi", tags=["Informasi"])
app.include_router(matkul_prak_routes.router, prefix="/v1/mata_kuliah", tags=["Mata Kuliah Praktikum"])
app.include_router(jadwal_routes.router, prefix="/v1/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_routes.router, prefix="/v1/nilai_akhir", tags=["Nilai Akhir"])
app.include_router(tugas_routes.router, prefix="/v1/tugas", tags=["Tugas"])
app.include_router(user_routes.router, prefix="/v1/user", tags=["User"])
app.include_router(auth_routes.router, prefix="/v1/auth", tags=["Auth"])
