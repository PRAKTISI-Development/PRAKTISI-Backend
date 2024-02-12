from pydantic import BaseModel, Field
from typing import Optional

class StudentSchema(BaseModel):
    NIM: Optional[str]
    nama_lengkap: Optional[str]
    semester: Optional[str]
    praktikum: Optional[str]
    kehadiran: Optional[float]
    proyek_akhir: Optional[float]
    nilai_akhir: Optional[float]