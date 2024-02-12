from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from apps.database import get_db
from apps.models.users import User
from apps.schemas.user_schema import UserSchema
from apps.controllers.users_controller import create_user, get_user
from apps.middleware.authentication import check_user_role
from apps.helpers.response import response
import requests
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict) -> dict:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=15)})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm='HS256')
    return {'token': encoded_jwt}

def verify_token(token: dict = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        userid: str = payload.get("nim")
        if userid is None:
            raise credentials_exception
        token_data = {"userid": userid}
        return token_data
    except JWTError:
        raise credentials_exception

def authenticate_user(request, userid: str, password: str, db: Session = Depends(get_db)):
    try:
        auth_payload = {"userid": userid, "password": password}
        headers = {"api-key": os.getenv("API_KEY")}
        is_dosen = len(userid) > 10
        is_praktikan = len(userid) == 10

        auth_response = requests.post(os.getenv("AUTH_SERVER"), json=auth_payload, headers=headers)
        if auth_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        userdata = auth_response.json().get('userdata')
        data = {
            "userid": userid,
            "password": password,
            "nama": userdata.get('nama'),
            "email": userdata.get('email'),
            "semester": userdata.get('semester'),
            "praktikan": is_praktikan,
            "asisten_laboratorium": False,
            "dosen": is_dosen,
            "kd_matkul": None
        }
        user = get_user(userid, db)
        if not user:
            create_user(UserSchema(**data), db)

        access_token = auth_response.json().get("token")
        if not access_token:
            raise HTTPException(status_code=401, detail="Access token not found in the response")

        status = check_user_role(user)
        own_access_token = create_access_token(data={"nim": userid, "status": status.get('status')})

        verify_token(own_access_token['token'])
        return own_access_token

    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

    
def get_current_user(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    userid = token_data.get("userid")
    user = db.query(User).filter(User.userid == userid).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return UserSchema(username=user.username, email=user.email)
