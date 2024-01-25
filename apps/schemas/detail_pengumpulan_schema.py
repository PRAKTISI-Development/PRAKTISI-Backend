from pydantic import BaseModel
from datetime import datetime

class DetailPengumpulanSchema(BaseModel):
    usersid: str
    kd_tugas: str
    file_tugas: str

    class Config:
        orm_mode = True
