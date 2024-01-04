from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum, auto
from apps.database import Base

class UserType(PyEnum):
    aslab = auto()
    praktikan = auto()

class User(Base):
    __tablename__ = "user"

    nim = Column(String, primary_key=True, index=True)
    password = Column(String)
    nama = Column(String)
    semester = Column(Integer)
    tipe_user = Column(Enum(UserType, name="tipe_user"))

    praktikan = relationship("Praktikan", back_populates="user")
    aslab = relationship("Aslab", back_populates="user")
