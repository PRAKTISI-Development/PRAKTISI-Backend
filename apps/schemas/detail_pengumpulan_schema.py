from pydantic import BaseModel, Field
from typing import Optional
from fastapi import File, UploadFile, Form

class DetailPengumpulanSchema(BaseModel):
    usersid: str
    kd_tugas: str
    file_tugas: Optional[str]
    file: Optional[UploadFile]
    file_path: Optional[str] = Field(None, alias="file_path")

    @classmethod
    def as_form(
        cls,
        usersid: str = Form(...),
        kd_tugas: str = Form(...),
        file_tugas: Optional[str] = Form(...),
        file: Optional[UploadFile] = File(...)
    ):
        return cls(
            usersid=usersid,
            kd_tugas=kd_tugas,
            file_tugas=file_tugas,
            file=file
        )

    class Config:
        orm_mode = True
