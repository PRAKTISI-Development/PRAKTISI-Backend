from sqlalchemy.orm import Session
from apps.models.aslab import Aslab
from apps.models.user import User
from apps.database import SessionLocal

def create_aslab(db: Session, aslab_data: Aslab):
    db_aslab = Aslab(**aslab_data)
    db.add(db_aslab)
    db.commit()
    db.refresh(db_aslab)
    return db_aslab

def get_aslab(db: Session, nim: str):
    return db.query(Aslab).filter(Aslab.nim == nim).first()

def get_aslabs(db: Session):
    return db.query(Aslab).all()

def update_aslab(db: Session, nim: str, aslab_data: Aslab):
    db_aslab = db.query(Aslab).filter(Aslab.nim == nim).first()
    for key, value in aslab_data.items():
        setattr(db_aslab, key, value)
    db.commit()
    db.refresh(db_aslab)
    return db_aslab

def delete_aslab(db: Session, nim: str):
    db_aslab = db.query(Aslab).filter(Aslab.nim == nim).first()
    db.delete(db_aslab)
    db.commit()
    return {"message": "Aslab deleted successfully"}

