from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.aslab import Aslab
from app.models.user import User
from app.database import SessionLocal, engine
from app.services import auth_service

def login(form_data: auth_service.OAuth2PasswordRequestForm = auth_service.Depends()):
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
