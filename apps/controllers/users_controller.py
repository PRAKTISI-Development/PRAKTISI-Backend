from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.users import User
from functools import lru_cache

async def create_user(user_data: User, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data (User): User data to be created.
        db (Session): Database session.

    Returns:
        User: Created user.

    Raises:
        HTTPException: If an internal server error occurs during database operations.
    """
    try:
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        # raise HTTPException(status_code=500, detail="Internal Server Error")
        print(e)

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

