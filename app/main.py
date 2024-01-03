from fastapi import FastAPI
from app.controllers import aslab_controller, praktikan_controller
from app.models import aslab, praktikan, jadwal, mata_kuliah, nilai_akhir, tugas, user
from app.services import aslab_service, praktikan_service, auth_service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(aslab_controller.router, prefix="/aslab", tags=["Aslab"])
app.include_router(praktikan_controller.router, prefix="/praktikan", tags=["Praktikan"])
