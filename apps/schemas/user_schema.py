from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    userid: str
    nama: str
    email: EmailStr
    semester: str
    praktikan: bool
    asisten_laboratorium: bool
    dosen: bool
    kd_matkul: str

    class Config:
        orm_mode = True
