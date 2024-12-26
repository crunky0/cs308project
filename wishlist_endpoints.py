from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import database

# Create APIRouter instance for wishlist-related endpoints
router = APIRouter()

# Load SQL from file function
def load_sql_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()

# Wishlist item model
class WishlistItem(BaseModel):
    userid: int
    productid: int

# Add to wishlist endpoint
@router.post("/wishlist/add")
async def add_to_wishlist(item: WishlistItem):
    sql_query = load_sql_file("sql/add_to_wishlist.sql")
    try:
        await database.execute(query=sql_query, values={"userid": item.userid, "productid": item.productid})
        return {"message": "Item added to wishlist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding to wishlist: {str(e)}")

# Remove from wishlist endpoint
@router.delete("/wishlist/remove")
async def remove_from_wishlist(item: WishlistItem):
    sql_query = load_sql_file("sql/remove_from_wishlist.sql")
    try:
        result = await database.execute(query=sql_query, values={"userid": item.userid, "productid": item.productid})
        if result == 0:
            raise HTTPException(status_code=404, detail="Item not found in wishlist")
        return {"message": "Item removed from wishlist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error removing from wishlist: {str(e)}")

@router.get("/wishlist/{userid}")
async def get_wishlist(userid: int):
    sql_query = load_sql_file("sql/fetch_wishlist.sql")
    try:
        items = await database.fetch_all(query=sql_query, values={"userid": userid})
        return [dict(item) for item in items]  # Convert results to a list of dictionaries
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching wishlist: {str(e)}")
