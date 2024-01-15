from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TugasSchema(BaseModel):
    kd_tugas: str
    jenis_tugas: Enum('Post Test', 'Proyek Akhir')
    nama_tugas: str
    deskripsi_tugas: str
    tanggal_dibuat: datetime
    tanggal_pengumpulan: datetime
    kd_matkul: str

    class Config:
        orm_mode = True
