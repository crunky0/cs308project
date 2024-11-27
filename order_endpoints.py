from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from db import database  # Import the Database instance
from order_service import OrderService

# Pydantic Models for request validation
class OrderItemRequest(BaseModel):
    productid: int
    quantity: int
    price: float

class OrderRequest(BaseModel):
    userid: int
    totalamount: float
    items: List[OrderItemRequest]

router = APIRouter()

@router.post("/create_order")
async def create_order(order_data: OrderRequest):
    """
    Endpoint to create an order.

    Args:
        order_data (OrderRequest): Data for the order, including user ID, total amount, and items.

    Returns:
        dict: Confirmation message with the created order ID.

    Raises:
        HTTPException: For stock issues or database errors.
    """
    order_service = OrderService(database)
    try:
        response = await order_service.create_order(order_data.dict())
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))