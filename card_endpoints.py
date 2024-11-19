from fastapi import FastAPI, HTTPException, APIRouter
from databases import Database
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

router = APIRouter()
# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "")
database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    if not database.is_connected:
        await database.connect()
    yield
    # Disconnect from the database
    if database.is_connected:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Pydantic model for adding to card
class AddToCard(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@router.post("/card/add")
async def add_to_card(item: AddToCard):
    # Step 1: Check if the product exists and has sufficient stock
    find_product_query = "SELECT * FROM products WHERE productid = :product_id"
    product = await database.fetch_one(query=find_product_query, values={"product_id": item.product_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["stock"] < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Step 2: Insert into card
    add_to_card_query = """
    INSERT INTO card (user_id, product_id, quantity)
    VALUES (:user_id, :product_id, :quantity)
    RETURNING user_id, product_id, quantity
    """
    new_item = await database.fetch_one(query=add_to_card_query, values={"user_id": item.user_id, "product_id": item.product_id, "quantity": item.quantity})

    # Step 3: Decrease the stock of the product
    update_stock_query = """
    UPDATE products SET stock = stock - :quantity WHERE productid = :product_id
    """
    await database.execute(query=update_stock_query, values={"quantity": item.quantity, "product_id": item.product_id})

    # Step 4: Return a detailed confirmation message with added item and stock update
    return {
        "message": "Item added to card successfully.",
        "details": {
            "added_item": {
                "user_id": new_item["user_id"],
                "product_id": new_item["product_id"],
                "quantity": new_item["quantity"]
            },
            "product_stock_updated": f"Stock for product_id {item.product_id} decreased by {item.quantity}."
        }
    }


