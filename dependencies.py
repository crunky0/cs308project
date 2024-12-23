# dependencies.py
from fastapi import Depends, HTTPException, status
from databases import Database

from db import database  # same database instance

def get_database() -> Database:
    """
    Return the global Database instance as a dependency.
    """
    return database

async def product_manager_required(
    user_id: int,                 # e.g. extracted from JWT in real usage
    db: Database = Depends(get_database)
):
    query = "SELECT role FROM users WHERE userid = :userid"
    row = await db.fetch_one(query, {"userid": user_id})
    if not row or row["role"] != "productmanager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized as product manager."
        )
    # Return user_id or user record
    return user_id
