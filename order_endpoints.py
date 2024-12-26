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

# Pydantic Models for response
class OrderItemResponse(BaseModel):
    productid: int
    productname: str
    image: str
    quantity: int
    price: float

class OrderResponse(BaseModel):
    orderid: int
    userid: int
    totalamount: float
    status: str
    items: List[OrderItemResponse]

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

@router.get("/orders/{userid}", response_model=List[OrderResponse])
async def get_orders_for_user(userid: int):
    """
    Endpoint to fetch all orders for a specific user with product details, including images and order status.

    Args:
        userid (int): The user ID to fetch orders for.

    Returns:
        List[OrderResponse]: List of orders with product details.

    Raises:
        HTTPException: If the user has no orders or an internal error occurs.
    """
    order_service = OrderService(database)
    try:
        orders = await order_service.get_orders_for_user(userid)
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for the user")
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))