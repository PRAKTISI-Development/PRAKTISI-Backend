from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.controllers.users_controller import *
from apps.helpers.response import response
from apps.schemas.user_schema import UserSchema


# Define the APIRouter
router = APIRouter()

# Define the create_user_endpoint function
@router.post("/", response_model=UserSchema)
def create_user_endpoint(user_data: UserSchema, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data (UserSchema): The user data to create.
        db (Session): The database session.

    Returns:
        UserSchema: The created user.
    """
    user = create_user(user_data, db)
    return user


# Define the read_user_endpoint function
@router.get("/{userid}", response_model=None)
async def read_user_endpoint(userid: str, db: Session = Depends(get_db)):
    """
    Read a user.

    Args:
        userid (str): The user ID.
        db (Session): The database session.

    Returns:
        UserSchema: The user data.
    """
    user = await get_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="User berhasil ditemukan!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

# Define the read_all_users_endpoint function
@router.get("/", response_model=None)
async def read_all_users_endpoint(db: Session = Depends(get_db)):
    """
    Read all users.

    Args:
        db (Session): The database session.

    Returns:
        UserSchema: The list of users.
    """
    users = await get_all_users(db)
    if users:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil ditemukan!", data=users)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

# Define the update_user_endpoint function
@router.put("/{userid}", response_model=None)
async def update_user_endpoint(userid: str, user_data: UserSchema, db: Session = Depends(get_db)):
    """
    Update a user.

    Args:
        userid (str): The user ID.
        user_data (UserSchema): The updated user data.
        db (Session): The database session.

    Returns:
        UserSchema: The updated user data.
    """
    user = update_user(user_data, userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil diperbarui!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

# Define the delete_user_endpoint function
@router.delete("/{userid}", response_model=None)
def delete_user_endpoint(userid: str, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        userid (str): The user ID.
        db (Session): The database session.

    Returns:
        UserSchema: The deleted user data.
    """
    user = delete_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil dihapus!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/{userid}", response_model=None)
async def read_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = await get_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="User berhasil ditemukan!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.get("/", response_model=None)
async def read_all_users_endpoint(db: Session = Depends(get_db)):
    users = await get_all_users(db)
    if users:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil ditemukan!", data=users)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.put("/{userid}", response_model=None)
async def update_user_endpoint(userid: str, user_data: UserSchema, db: Session = Depends(get_db)):
    user = update_user(user_data, userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil diperbarui!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)

@router.delete("/{userid}", response_model=None)
def delete_user_endpoint(userid: str, db: Session = Depends(get_db)):
    user = delete_user(userid, db)
    if user:
        try:
            return response(status_code=200, success=True, msg="Data User berhasil dihapus!", data=user)
        except HTTPException as e:
            return response(status_code=e.status_code, success=False, msg=e.detail, data=None)
