import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import asyncpg
from databases import Database



# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)
# FastAPI app initialization
app = FastAPI()

# Pydantic models for request bodies
class Category(BaseModel):
    categoryid: int
    name: str

class Product(BaseModel):
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

# Load SQL from file function
def load_sql_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


# Connect to the database when the app starts
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

# Disconnect from the database when the app shuts down
@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

# API Endpoint to search products by category
@app.get("/search/by_category/{category_name}")
async def get_products_by_category(category_name: str):


    # Check if the category exists
    find_product_by_category_query = load_sql_file('sql/find_product_by_category.sql')
    all_products_by_category = await database.fetch_all(query=find_product_by_category_query, values={"category_name": category_name})
    
    if not all_products_by_category:
        raise HTTPException(status_code=400, detail="No product can be found in the given category.")


    
    return [Product(**dict(product)) for product in all_products_by_category]

