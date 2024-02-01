from enum import Enum
from pydantic import BaseModel

class StatusEnum(str, Enum):
    Hadir = 'Hadir'
    Tidak_Hadir = 'Tidak Hadir'

class KehadiranSchema(BaseModel):
    usersid: str
    kd_jadwal: str
    status: StatusEnum
    keterangan: str

    class Config:
        orm_mode = True

