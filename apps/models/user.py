from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum, auto
from apps.database import Base

class UserType(PyEnum):
    aslab = auto()
    praktikan = auto()

class User(Base):
    __tablename__ = "user"

    nim: str = Column(String, primary_key=True, index=True)
    password: str = Column(String)
    nama: str = Column(String)
    semester: int = Column(Integer)
    tipe_user: Enum = Column(Enum(UserType, name="tipe_user"))

    praktikan: str = relationship("Praktikan", back_populates="user")
    aslab: str = relationship("Aslab", back_populates="user")
