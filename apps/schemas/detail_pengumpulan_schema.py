from pydantic import BaseModel, Field
from typing import Optional
from fastapi import File, UploadFile, Form

class DetailPengumpulanSchema(BaseModel):
    usersid: str
    kd_tugas: str
    link_tugas: Optional[str] = Field(None,alias='link_tugas')
    file: Optional[UploadFile] = Field(None,alias='file')
    file_path: Optional[str] = Field(None, alias="file_path")

    @classmethod
    def as_form(
        cls,
        usersid: str = Form(...),
        kd_tugas: str = Form(...),
        link_tugas: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None)
    ):
        return cls(
            usersid=usersid,
            kd_tugas=kd_tugas,
            link_tugas=link_tugas,
            file=file
        )

    class Config:
        orm_mode = True
