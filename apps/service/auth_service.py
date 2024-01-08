from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.users import TokenData
from apps.models.user import User
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Dependency untuk mendapatkan token dari header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fungsi untuk memverifikasi token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return token_data

def get_user(db: Session, username: str):
    return user_controller.get_user_by_nim(db, username)

# Fungsi untuk memverifikasi kata sandi
def verify_password(plain_password, hashed_password):
    # Implementasi verifikasi kata sandi sesuai kebutuhan aplikasi Anda
    # Contoh sederhana: return plain_password == hashed_password
    return True

# Fungsi untuk mendapatkan role (tipe_user) user
def get_user_role(db: Session, username: str):
    user = get_user(db, username)
    if user:
        return user.tipe_user
    return None

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

