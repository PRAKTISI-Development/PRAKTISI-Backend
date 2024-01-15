from pydantic import BaseModel

class NilaiAkhirSchema(BaseModel):
    usersid: str
    kd_matkul: str
    nilai_akhir: int

    class Config:
        orm_mode = True
