from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from databases import Database
from db import database

# Pydantic models for requests and responses
class CancelRequest(BaseModel):
    orderid: int

class CancelResponse(BaseModel):
    orderid: int
    status: str
    message: Optional[str] = None

# Create an APIRouter instance
router = APIRouter()

@router.post("/order/cancel", response_model=CancelResponse)
async def request_cancel_order(cancel_request: CancelRequest):
    """
    User requests to cancel an order.

    Args:
        cancel_request (CancelRequest): Contains the order ID.

    Returns:
        CancelResponse: Status of the cancellation request.
    """
    query_check_status = """
        SELECT status FROM orders WHERE orderid = :orderid
    """
    order_status = await database.fetch_one(query_check_status, {"orderid": cancel_request.orderid})

    if not order_status:
        raise HTTPException(status_code=404, detail="Order not found.")

    if order_status["status"] != "processing":
        raise HTTPException(status_code=400, detail="Order cannot be canceled as it is not in processing status.")

    try:
        async with database.transaction():
            # Retrieve order items before deletion
            query_get_order_items = """
                SELECT productid, quantity FROM order_items WHERE orderid = :orderid
            """
            order_items = await database.fetch_all(query_get_order_items, {"orderid": cancel_request.orderid})

            # Update the stock
            for item in order_items:
                query_update_stock = """
                    UPDATE products SET stock = stock + :quantity WHERE productid = :productid
                """
                await database.execute(query_update_stock, {
                    "quantity": item["quantity"],
                    "productid": item["productid"]
                })

            # Delete items related to the order
            query_delete_items = """
                DELETE FROM order_items WHERE orderid = :orderid
            """
            await database.execute(query_delete_items, {"orderid": cancel_request.orderid})

            # Delete the order
            query_delete_order = """
                DELETE FROM orders WHERE orderid = :orderid
            """
            await database.execute(query_delete_order, {"orderid": cancel_request.orderid})

        return CancelResponse(orderid=cancel_request.orderid, status="Canceled", message="Order has been canceled and stock updated.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")