from fastapi import APIRouter, Depends
from apps.controllers.user_controller import user
from fastapi.security import OAuth2PasswordBearer
from service.auth_service import *
from apps.controllers import user_controller
from apps.database import get_db

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    db = get_db()
    user = user_controller.get_user_by_nim(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": user.nim,
        "tipe_user": user.tipe_user,
    }
    return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}
