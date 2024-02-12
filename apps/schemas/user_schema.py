from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    userid: str = None
    nama: str
    email: EmailStr
    password: str
    semester: str
    praktikan: bool
    asisten_laboratorium: bool
    dosen: bool
    kd_matkul: Optional[str]

    class Config:
        orm_mode = True
