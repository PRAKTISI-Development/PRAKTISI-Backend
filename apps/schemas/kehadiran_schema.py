from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class KehadiranSchema(BaseModel):
    usersid: str
    kd_jadwal: str
    pertemuan: int
    materi: str
    tanggal: datetime
    keterangan: Enum('Hadir', 'Tidak Hadir')

    class Config:
        orm_mode = True
