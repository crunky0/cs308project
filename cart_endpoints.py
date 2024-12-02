from fastapi import FastAPI, HTTPException, APIRouter
from databases import Database
from pydantic import BaseModel
from db import database

router = APIRouter()

# Pydantic model for adding to cart
class AddToCart(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

@router.post("/cart/add")
async def add_to_cart(item: AddToCart):
    # Step 1: Check if the product exists and has sufficient stock
    find_product_query = "SELECT * FROM products WHERE productid = :product_id"
    product = await database.fetch_one(query=find_product_query, values={"product_id": item.product_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["stock"] <= 0:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    # Step 2: Insert or update the cart
    existing_cart_query = """
    SELECT * FROM cart WHERE user_id = :user_id AND product_id = :product_id
    """
    existing_item = await database.fetch_one(query=existing_cart_query, values={"user_id": item.user_id, "product_id": item.product_id})

    if existing_item:
        update_cart_query = """
        UPDATE cart SET quantity = quantity + :quantity 
        WHERE user_id = :user_id AND product_id = :product_id
        """
        await database.execute(query=update_cart_query, values={"quantity": item.quantity, "user_id": item.user_id, "product_id": item.product_id})
    else:
        add_to_cart_query = """
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (:user_id, :product_id, :quantity)
        """
        await database.execute(query=add_to_cart_query, values={"user_id": item.user_id, "product_id": item.product_id, "quantity": item.quantity})

    return {"message": "Item added to cart successfully."}

@router.post("/cart/increase")
async def increase_cart(user_id: int, product_id: int):
    # Check product stock
    find_product_query = "SELECT stock FROM products WHERE productid = :product_id"
    product = await database.fetch_one(query=find_product_query, values={"product_id": product_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_query = "SELECT * FROM cart WHERE user_id = :user_id AND product_id = :product_id"
    cart_item = await database.fetch_one(query=cart_query, values={"user_id": user_id, "product_id": product_id})

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if cart_item["quantity"] + 1 > product["stock"]:
        raise HTTPException(status_code=400, detail="Insufficient stock for this operation")

    update_cart_query = "UPDATE cart SET quantity = quantity + 1 WHERE user_id = :user_id AND product_id = :product_id"
    await database.execute(query=update_cart_query, values={"user_id": user_id, "product_id": product_id})

    return {"message": "Quantity increased by 1."}

@router.post("/cart/decrease")
async def decrease_cart(user_id: int, product_id: int):
    cart_query = "SELECT * FROM cart WHERE user_id = :user_id AND product_id = :product_id"
    cart_item = await database.fetch_one(query=cart_query, values={"user_id": user_id, "product_id": product_id})

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if cart_item["quantity"] - 1 <= 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be less than 1")

    update_cart_query = "UPDATE cart SET quantity = quantity - 1 WHERE user_id = :user_id AND product_id = :product_id"
    await database.execute(query=update_cart_query, values={"user_id": user_id, "product_id": product_id})

    return {"message": "Quantity decreased by 1."}

@router.delete("/cart/remove")
async def remove_cart_item(user_id: int, product_id: int):
    cart_query = "SELECT * FROM cart WHERE user_id = :user_id AND product_id = :product_id"
    cart_item = await database.fetch_one(query=cart_query, values={"user_id": user_id, "product_id": product_id})

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    delete_query = "DELETE FROM cart WHERE user_id = :user_id AND product_id = :product_id"
    await database.execute(query=delete_query, values={"user_id": user_id, "product_id": product_id})

    return {"message": "Item removed from cart."}

@router.get("/cart")
async def get_cart(user_id: int):
    cart_query = """
    SELECT c.product_id, c.quantity, p.name, p.stock, p.price
    FROM cart c
    JOIN products p ON c.product_id = p.productid
    WHERE c.user_id = :user_id
    """
    items = await database.fetch_all(query=cart_query, values={"user_id": user_id})

    if not items:
        return {"message": "Cart is empty", "cart": []}

    cart_details = [
        {
            "product_id": item["product_id"],
            "name": item["name"],
            "quantity": item["quantity"],
            "stock": item["stock"],
            "price": item["price"],
            "total_price": item["quantity"] * item["price"]
        }
        for item in items
    ]

    total_cart_price = sum(item["total_price"] for item in cart_details)

    return {
        "cart": cart_details,
        "total_cart_price": total_cart_price
    }