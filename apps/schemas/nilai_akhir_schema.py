from pydantic import BaseModel

class NilaiAkhirSchema(BaseModel):
    usersid: str
    kd_matkul: str
    nilai_akhir: float

    class Config:
        orm_mode = True
