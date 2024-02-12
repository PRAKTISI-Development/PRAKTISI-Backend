from pydantic import BaseModel
from typing import List

class MatkulPrakSchema(BaseModel):
    kd_matkul: str = None
    nama_matkul: str

    class Config:
        orm_mode = True
