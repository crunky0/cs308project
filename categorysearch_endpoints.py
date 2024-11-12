from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from db import database


# Create APIRouter instance for user-related endpoints
router = APIRouter()


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



# API Endpoint to search products by category
@router.get("/search/by_category/{category_name}")
async def get_products_by_category(category_name: str):


    # Check if the category exists
    find_product_by_category_query = load_sql_file('sql/find_product_by_category.sql')
    all_products_by_category = await database.fetch_all(query=find_product_by_category_query, values={"category_name": category_name})
    
    if not all_products_by_category:
        raise HTTPException(status_code=400, detail="No product can be found in the given category.")


    
    return [Product(**dict(product)) for product in all_products_by_category]

