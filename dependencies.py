# dependencies.py (example)
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from db import database

def get_current_user(db: Session = Depends(database)):
    """
    Normally, you'd decode a JWT or retrieve from session here.
    For demonstration, we will just pick a user that has role='productmanager'.
    """
    user = db.query(User).filter(User.role == "productmanager").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

def product_manager_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "productmanager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized as product manager"
        )
    return current_user
