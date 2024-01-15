from datetime import date, time
from pydantic import BaseModel
from typing import Optional

class JadwalSchema(BaseModel):
    kd_jadwal: str
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time
    ruangan: str
    kd_matkul: str

    class Config:
        orm_mode = True
