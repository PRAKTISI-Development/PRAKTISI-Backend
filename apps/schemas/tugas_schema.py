from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from apps.helpers.generator import identity_generator

class JenistugasEnum(str, Enum):
    Hadir = 'Post Test'
    Tidak_Hadir = 'Proyek Akhir'

class TugasSchema(BaseModel):
    kd_tugas: str = identity_generator()
    jenis_tugas: JenistugasEnum
    nama_tugas: str
    deskripsi_tugas: str
    tanggal_dibuat: datetime
    tanggal_pengumpulan: datetime
    kd_matkul: str

    class Config:
        orm_mode = True
