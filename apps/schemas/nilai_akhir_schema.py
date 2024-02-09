from pydantic import BaseModel, Field
from typing import Optional

class NilaiAkhirSchema(BaseModel):
    usersid: str = None
    kd_matkul: str = None
    nilai_akhir: Optional[float] = Field(0,alias="nilai_akhir")

    class Config:
        orm_mode = True
