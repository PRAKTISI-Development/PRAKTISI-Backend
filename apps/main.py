from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from apps.database import Base, engine
from apps.routes import *
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="apps/templates")

app = FastAPI(
    title="REST SERVER PRAKTISI",
    debug=True,
    version="1.0.0",
    description="PRAKTISI Backend Web Application",
    docs_url="/docs",
    redoc_url="/documentations",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="apps/public"), name="public")
app.mount("/404", StaticFiles(directory="apps/templates"), name="404")

@app.get("/redocs", response_class=HTMLResponse)
async def redocs():
    return await HTMLResponse(content="This is your Redoc page.")

@app.get('/')
async def root():
    return RedirectResponse(url='/redocs')

@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    data = {"detail": "not found"}
    return templates.TemplateResponse("404.html", {"request": request, "data" : data}, status_code=404)

Base.metadata.create_all(bind=engine)
app.include_router(detail_pengumpulan_routes.router, prefix="/v1/detail_pengumpulan", tags=["Detail Pengumpulan"])
app.include_router(kehadiran_routes.router, prefix="/v1/kehadiran", tags=["Kehadiran"])
app.include_router(informasi_routes.router, prefix="/v1/informasi", tags=["Informasi"])
app.include_router(matkul_prak_routes.router, prefix="/v1/mata_kuliah", tags=["Mata Kuliah Praktikum"])
app.include_router(jadwal_routes.router, prefix="/v1/jadwal", tags=["Jadwal"])
app.include_router(nilai_akhir_routes.router, prefix="/v1/nilai_akhir", tags=["Nilai Akhir"])
app.include_router(tugas_routes.router, prefix="/v1/tugas", tags=["Tugas"])
app.include_router(user_routes.router, prefix="/v1/user", tags=["User"])
