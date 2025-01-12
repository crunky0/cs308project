from fastapi import APIRouter, HTTPException
from db import database
from pydantic import BaseModel
import os
from typing import Optional

    
class DiscountRequest(BaseModel):
    discountPrice: float

router = APIRouter()

# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()


# Pydantic model for adding a product
class ProductCreate(BaseModel):
    serialnumber: int
    productname: str
    productmodel: str
    description: str
    distributerinfo: str
    warranty: str
    price: float
    cost: float
    stock: int
    categoryid: int
    soldamount: int
    discountprice: Optional[float]  # Optional field for discount
    image: str

# Get product by ID
@router.get("/products/{product_id}/")
async def get_product_by_id(product_id: int):
    query = load_sql_file("get_product_by_id.sql")
    product = await database.fetch_one(query=query, values={"productID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(product)

# Search products by name (partial match)
@router.get("/products/search/name/")
async def search_products_by_name(productName: str):
    query = load_sql_file("search_product_by_name.sql")
    products = await database.fetch_all(query=query, values={"productName": productName})
    return [dict(product) for product in products]

# Search products by description (partial match)
@router.get("/products/search/description/")
async def search_products_by_description(description: str):
    query = load_sql_file("search_product_by_description.sql")
    products = await database.fetch_all(query=query, values={"description": description})
    return [dict(product) for product in products]

# Get all products
@router.get("/products/")
async def get_all_products():
    query = load_sql_file("get_all_products.sql")
    products = await database.fetch_all(query=query)
    return [dict(product) for product in products]

# Add a new product
@router.post("/products/")
async def add_product(product: ProductCreate):
    query = load_sql_file("add_product.sql")
    values = product.dict()
    new_product = await database.fetch_one(query=query, values=values)
    return dict(new_product)

# Remove a product
@router.delete("/products/{product_id}/")
async def remove_product(product_id: int):
    query = load_sql_file("remove_product.sql")
    product = await database.fetch_one(query=query, values={"productID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product removed successfully", "product": dict(product)}

# Add a discount to a product
@router.put("/products/{product_id}/discount/")
async def add_discount(product_id: int, discount: DiscountRequest):
    discountPrice = discount.discountPrice

    if discountPrice <= 0:
        raise HTTPException(status_code=400, detail="Discount price must be greater than 0")

    query = load_sql_file("add_discount.sql")
    product = await database.fetch_one(query=query, values={"productID": product_id, "discountPrice": discountPrice})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Discount added successfully", "product": dict(product)}

# Remove a discount from a product
@router.put("/products/{product_id}/discount/remove/")
async def remove_discount(product_id: int):
    query = load_sql_file("remove_discount.sql")
    product = await database.fetch_one(query=query, values={"productID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Discount removed successfully", "product": dict(product)}