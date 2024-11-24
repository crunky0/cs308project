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



# API Endpoint to search products by name
@router.get("/search/by_name/{product_name}")
async def get_products_by_name(product_name: str):


    # Check if the category exists
    find_products_by_name_query = load_sql_file('sql/find_products_by_name.sql')
    all_products_by_name= await database.fetch_all(query=find_products_by_name_query, values={"product_name": f"%{product_name}%"})
    
    if not all_products_by_name:
        raise HTTPException(status_code=400, detail="No product can be found in the given name.")


    
    return [Product(**dict(product)) for product in all_products_by_name]

# API Endpoint to search products by description.
@router.get("/search/by_description/{description}")
async def get_products_by_description(description: str):


    # Check if the category exists
    find_products_by_description_query = load_sql_file('sql/find_products_by_description.sql')
    all_products_by_description= await database.fetch_all(query=find_products_by_description_query, values={"description": f"%{description}%"})
    
    if not all_products_by_description:
        raise HTTPException(status_code=400, detail="No product can be found in the given description.")


    
    return [Product(**dict(product)) for product in all_products_by_description]

