from pydantic import BaseModel
from typing import List

class MatkulPrakSchema(BaseModel):
    kd_matkul: str
    nama_matkul: str
    usersid: str

    class Config:
        orm_mode = True
