from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order, OrderItem, Product
from db import database
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# Pydantic models for the order request
class OrderItemRequest(BaseModel):
    productid: int
    quantity: int
    price: float

class OrderRequest(BaseModel):
    userid: int
    totalamount: float
    items: List[OrderItemRequest]

# Endpoint to create an order
@router.post("/create_order")
async def create_order(order_data: OrderRequest):
    try:
        async with database.transaction():  # Begin transaction
            # Create the order instance (excluding 'items' since it belongs to the order_items table)
            order = Order(
                userid=order_data.userid,
                totalamount=order_data.totalamount
            )
            await database.execute(Order.__table__.insert(), order_data.dict(exclude={"items"}))  # Insert without 'items'
            
            # Query the order ID after the insert
            query = select(Order).where(Order.userid == order_data.userid).order_by(Order.orderid.desc()).limit(1)
            result = await database.fetch_one(query)
            if not result:
                raise HTTPException(status_code=400, detail="Failed to create order")

            orderid = result["orderid"]  # Use the order ID of the newly created order

            # Add order items and update stock
            for item in order_data.items:
                # Check if the product exists and has enough stock
                product = await database.fetch_one(select(Product).where(Product.productid == item.productid))

                if product and product["stock"] >= item.quantity:
                    # Insert the order item
                    order_item_values = {
                        "orderid": orderid,
                        "productid": item.productid,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    await database.execute(OrderItem.__table__.insert(), order_item_values)

                    # Update the product stock
                    updated_stock = product["stock"] - item.quantity
                    await database.execute(
                        Product.__table__.update().where(Product.productid == item.productid).values(stock=updated_stock)
                    )
                else:
                    raise HTTPException(status_code=400, detail=f"Not enough stock for product {item.productid}")

            return {"orderid": orderid, "message": "Order created successfully"}

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors and rollback if necessary
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Catch any other exceptions
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")
