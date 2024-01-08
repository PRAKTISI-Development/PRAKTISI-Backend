from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from apps.database import Base
from typing import List

class UserType(Enum):
    aslab = "aslab"
    praktikan = "praktikan"

class User(Base):
    __tablename__ = "user"

    nim = Column(String, primary_key=True, index=True)
    password = Column(String)
    nama = Column(String)
    semester = Column(Integer)
    tipe_user = List[UserType]  # Tambahkan parameter name

    praktikan = relationship("Praktikan", back_populates="user")
    aslab = relationship("Aslab", back_populates="user")
