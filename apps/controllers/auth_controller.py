from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import requests
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from apps.database import get_db
from apps.models import users
from apps.schemas import user_schema
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=15)})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm='HS256')

    return {'token': encoded_jwt}

def verify_token(token_data: dict = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = token_data.get('token')
    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        userid: str = payload.get("nim")
        if userid is None:
            raise credentials_exception

        token_data = {"userid": userid}
        return token_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})

    except jwt.InvalidTokenError:
        raise credentials_exception
def authenticate_user(userid: str, password: str):

    auth_payload = {"userid": userid,"password": password}
    headers = {"api-key": os.getenv("API_KEY")}

    auth_response = requests.post(os.getenv("AUTH_SERVER"), json=auth_payload, headers=headers)
    if auth_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth_response.json().get("token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found in the response")

    own_access_token = create_access_token(data={"nim": userid})

    # Verifying Token
    verify_token(own_access_token)

    return own_access_token

def get_current_user(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    userid = token_data.get("userid")
    user = db.query(users).filter(users.userid == userid).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user_schema(username=user.username, email=user.email)
