from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel
from databases import Database
from db import database

# Create APIRouter instance for user-related endpoints
router = APIRouter()

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


#API endpoint to get information about the selected products' stock.
@router.get("/products/{productID}")
async def get_stock(productID: int):
    sql_query = load_sql_file('sql/find_product.sql')
    product = await database.fetch_one(query=sql_query, values={"productID": productID})
    if product:
        product = Product(**dict(product))
        product = product.dict()
        if product["stock"] == 0:
            message = "Out of Stock."
        else:
            message = f"{product["stock"]} items available."
        return message
    else:
        raise HTTPException(status_code=400, detail="Selected product cannot be found.")
        