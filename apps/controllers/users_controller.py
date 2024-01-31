from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.users import User
from functools import lru_cache
from apps.schemas.user_schema import UserSchema
from fastapi.exceptions import HTTPException

def create_user(user_data: UserSchema, db: Session = Depends(get_db)):
    try:
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.flush()
        return db_user
    except HTTPException as e:
        print(e)
        db.rollback()
        # raise HTTPException(status_code=500, detail="Failed to create user")


@lru_cache
async def get_user(userid: str, db: Session = Depends(get_db)):
    """
    Get a user by userid.

    Args:
        userid (str): User ID to be retrieved.
        db (Session): Database session.

    Returns:
        User: Retrieved user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = db.query(User).filter(User.userid == userid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@lru_cache
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users.

    Args:
        db (Session): Database session.

    Returns:
        List[User]: List of all users.
    """
    users = db.query(User).all()
    return users

async def update_user(user_data: User, userid: str, db: Session = Depends(get_db)):
    """
    Update a user by userid.

    Args:
        user_data (User): User data to be updated.
        userid (str): User ID to be updated.
        db (Session): Database session.

    Returns:
        User: Updated user.

    Raises:
        HTTPException: If the user is not found or an internal server error occurs during database operations.
    """
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_user(userid: str, db: Session = Depends(get_db)):
    """
    Delete a user by userid.

    Args:
        userid (str): User ID to be deleted.
        db (Session): Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the user is not found or an internal server error occurs during database operations.
    """
    db_user = db.query(User).filter(User.userid == userid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

