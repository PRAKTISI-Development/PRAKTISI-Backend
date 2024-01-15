from pydantic import BaseModel
from datetime import datetime

class DetailPengumpulanSchema(BaseModel):
    usersid: str
    kd_tugas: str
    tanggal_pengumpulan: datetime
    file_path: str

    class Config:
        orm_mode = True
