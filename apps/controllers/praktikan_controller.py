from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from apps.models.aslab import Aslab
from apps.models.user import User
from apps.database import SessionLocal, engine
from apps.service import auth_service
from apps.models.praktikan import Praktikan

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

def create_praktikan(db: Session, praktikan_data: Praktikan):
    db_praktikan = Praktikan(**praktikan_data.dict())
    db.add(db_praktikan)
    db.commit()
    db.refresh(db_praktikan)
    return db_praktikan

def get_praktikan(db: Session, nim: str):
    return db.query(Praktikan).filter(Praktikan.nim == nim).first()

def get_praktikans(db: Session):
    return db.query(Praktikan).all()

def update_praktikan(db: Session, nim: str, praktikan_data: Praktikan):
    db_praktikan = db.query(Praktikan).filter(Praktikan.nim == nim).first()
    for key, value in praktikan_data.dict().items():
        setattr(db_praktikan, key, value)
    db.commit()
    db.refresh(db_praktikan)
    return db_praktikan

def delete_praktikan(db: Session, nim: str):
    db_praktikan = db.query(Praktikan).filter(Praktikan.nim == nim).first()
    db.delete(db_praktikan)
    db.commit()
    return {"message": "Praktikan deleted successfully"}
