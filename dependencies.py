# dependencies.py
from fastapi import HTTPException, status
from db import database # same database instance


async def product_manager_required(
    user_id: int,                 # e.g. extracted from JWT in real usage
):
    query = "SELECT role FROM users WHERE userid = :userid"
    row = await database.fetch_one(query, {"userid": user_id})
    if not row or row["role"] != "Productmanager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized as product manager."
        )
    # Return user_id or user record
    return user_id
