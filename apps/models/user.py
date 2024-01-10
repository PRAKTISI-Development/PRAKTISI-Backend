from sqlalchemy import Column, String, Integer
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from apps.database import Base
from enum import Enum as PyEnum, auto

class UserType(PyEnum):
    aslab = auto()
    praktikan = auto()

class User(Base):
    __tablename__ = "user"

    nim = Column(String(length=10), primary_key=True, index=True)
    password = Column(String(length=255))
    nama = Column(String(length=255))
    semester = Column(Integer)
    tipe_user = Column(Enum(UserType, name="user_type"))

    praktikan = relationship("Praktikan", back_populates="user")
    aslab = relationship("Aslab", back_populates="user")
