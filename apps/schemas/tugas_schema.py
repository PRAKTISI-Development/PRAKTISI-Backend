from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from apps.helpers.generator import identity_generator

class TugasSchema(BaseModel):
    kd_tugas: str = identity_generator()
    jenis_tugas: Enum('Post Test', 'Proyek Akhir')
    nama_tugas: str
    deskripsi_tugas: str
    tanggal_dibuat: datetime
    tanggal_pengumpulan: datetime
    kd_matkul: str

    class Config:
        orm_mode = True
