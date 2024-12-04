from fastapi import APIRouter, HTTPException
from db import database
from pydantic import BaseModel
import os
from typing import List,Optional

router = APIRouter()

# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()

# Response model for products
class ProductResponse(BaseModel):
    productid: int
    serialnumber: int
    productname: str
    productmodel: str
    description: str
    distributerinfo: str
    warranty: str
    price: float
    stock: int
    categoryid: int
    soldamount: int
    discountprice: Optional[float]
    image: str

# Endpoint to get products by category ID
@router.get("/products/category/{category_id}/", response_model=List[ProductResponse])
async def get_products_by_category(category_id: int):
    query = load_sql_file("find_products_by_category.sql")
    products = await database.fetch_all(query=query, values={"categoryID": category_id})
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    
    return [dict(product) for product in products]
