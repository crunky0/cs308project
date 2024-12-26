from fastapi import APIRouter, HTTPException
from db import database
import os

router = APIRouter()

# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()

# Endpoint to get products sorted by price in ascending order
@router.get("/products/sort/price/asc/")
async def sort_products_by_price_asc():
    query = load_sql_file("sort_price_asc.sql")
    products = await database.fetch_all(query=query)
    return [dict(product) for product in products]

# Endpoint to get products sorted by price in descending order
@router.get("/products/sort/price/desc/")
async def sort_products_by_price_desc():
    query = load_sql_file("sort_price_desc.sql")
    products = await database.fetch_all(query=query)
    return [dict(product) for product in products]

# Endpoint to get products sorted by popularity (soldAmount) in ascending order
@router.get("/products/sort/popularity/asc/")
async def sort_products_by_popularity_asc():
    query = load_sql_file("sort_popularity_asc.sql")
    products = await database.fetch_all(query=query)
    return [dict(product) for product in products]

# Endpoint to get products sorted by popularity (soldAmount) in descending order
@router.get("/products/sort/popularity/desc/")
async def sort_products_by_popularity_desc():
    query = load_sql_file("sort_popularity_desc.sql")
    products = await database.fetch_all(query=query)
    return [dict(product) for product in products]
