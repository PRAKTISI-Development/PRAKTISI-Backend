from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base

class Praktikan(Base):
    __tablename__ = "praktikan"

    nim = Column(String, primary_key=True, index=True)

    user = relationship("User", back_populates="praktikan")
    nilai_akhir = relationship("NilaiAkhir", back_populates="praktikan")
