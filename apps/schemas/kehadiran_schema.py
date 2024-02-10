from enum import Enum
from pydantic import BaseModel

class StatusEnum(str, Enum):
    Hadir = 'Hadir'
    Tidak_Hadir = 'Tidak Hadir'

class KehadiranSchema(BaseModel):
    usersid: str = None
    kd_jadwal: str = None
    status: StatusEnum
    keterangan: str

    class Config:
        orm_mode = True

