from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.database import engine
from apps.routes import aslab_routes, jadwal_routes, mata_kuliah_routes, nilai_akhir_routes, praktikan_routes, tugas_routes, user_routes
from apps.database import Base

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

app.include_router(aslab_routes.router, prefix="/api/aslab", tags=["Aslab"])
app.include_router(praktikan_routes.router, prefix="/api/praktikan", tags=["Praktikan"])
app.include_router(mata_kuliah_routes.router, prefix="/api/mata_kuliah", tags=["Jadwal"])
app.include_router(jadwal_routes.router, prefix="/api/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_routes.router, prefix="/api/nilai_akhir", tags=["Nilai Akhir"])
app.include_router(tugas_routes.router, prefix="/api/tugas", tags=["Tugas"])
app.include_router(user_routes.router, prefix="/api/user", tags=["User"])
