from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from apps.models.aslab import Aslab
from apps.models.user import User
from apps.database import SessionLocal, engine
from apps.services import auth_service

def login(form_data: auth_service.OAuth2PasswordBearer = auth_service.Depends()):
    db = SessionLocal()

    user = db.query(User).filter(User.nim == form_data.username, User.tipe_user == "aslab").first()

    if user is None or not auth_service.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

def create_aslab(db: Session, aslab_data: Aslab):
    db_aslab = Aslab(**aslab_data.dict())
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
    for key, value in aslab_data.dict().items():
        setattr(db_aslab, key, value)
    db.commit()
    db.refresh(db_aslab)
    return db_aslab

def delete_aslab(db: Session, nim: str):
    db_aslab = db.query(Aslab).filter(Aslab.nim == nim).first()
    db.delete(db_aslab)
    db.commit()
    return {"message": "Aslab deleted successfully"}

