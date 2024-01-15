from datetime import datetime
from pydantic import BaseModel

class InformasiSchema(BaseModel):
    kd_informasi: str
    tanggal: datetime
    judul_informasi: str
    deskripsi_informasi: str
    tautan: str
    usersid: str

    class Config:
        orm_mode = True
