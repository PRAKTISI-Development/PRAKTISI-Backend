from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from apps.helpers.generator import identity_generator

class InformasiSchema(BaseModel):
    kd_informasi: str = identity_generator()
    tanggal: datetime
    judul_informasi: str
    deskripsi_informasi: str
    tautan: str
    usersid: str

    class Config:
        orm_mode = True
