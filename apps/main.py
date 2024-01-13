from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from apps.database import Base, engine
from apps.routes import detail_pengumpulan_routes, informasi_routes, jadwal_routes, kehadiran_routes, matkul_prak_routes, nilai_akhir_routes, tugas_routes, user_routes

app = FastAPI(
    title="REST-SERVER PRAKTISI",
    debug=True,
    version="1.0.0",
    description="PRAKTISI BACKEND APP",
    docs_url="/api_docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json",
)

@app.get('/')
async def root():
    return RedirectResponse(url='/redocs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(detail_pengumpulan_routes.router, prefix="/v1/detail_pengumpulan", tags=["Detail Pengumpulan"])
app.include_router(kehadiran_routes.router, prefix="/v1/kehadiran", tags=["Kehadiran"])
app.include_router(informasi_routes.router, prefix="/v1/praktikan", tags=["Informasi"])
app.include_router(matkul_prak_routes.router, prefix="/v1/mata_kuliah", tags=["Mata Kuliah Praktikum"])
app.include_router(jadwal_routes.router, prefix="/v1/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_routes.router, prefix="/v1/nilai_akhir", tags=["Nilai Akhir"])
app.include_router(tugas_routes.router, prefix="/v1/tugas", tags=["Tugas"])
app.include_router(user_routes.router, prefix="/v1/user", tags=["User"])
