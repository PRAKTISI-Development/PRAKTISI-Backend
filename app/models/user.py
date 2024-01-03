from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "user"

    nim = Column(String, primary_key=True, index=True)
    password = Column(String)
    nama = Column(String)
    semester = Column(Integer)
    tipe_user = Column(String)

    praktikan = relationship("Praktikan", back_populates="user")
    aslab = relationship("Aslab", back_populates="user")
