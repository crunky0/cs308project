from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from databases import Database
from typing import Dict
from db import database
from models import Order, OrderItem
from dependencies import product_manager_required

# Define a Pydantic model for refund requests
class RefundRequest(BaseModel):
    orderid: int
    reason: str

# Define a Pydantic model for refund responses
class RefundResponse(BaseModel):
    orderid: int
    refunded_amount: float
    status: str

# Create an APIRouter instance
router = APIRouter()

@router.post("/refund", response_model=RefundResponse)
async def process_refund(refund_request: RefundRequest, user_id: int = Depends(product_manager_required)):
    
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
    Endpoint to process a refund for a specific order.

    Args:
        refund_request (RefundRequest): Contains order ID and reason for refund.

    Returns:
        RefundResponse: Refund details including refunded amount and status.

    Raises:
        HTTPException: If the order does not exist or cannot be refunded.
    
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
    try:
        # Fetch the order details
        query_order = 
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
            SELECT orderid, total_amount
            FROM orders
            WHERE orderid = :orderid
        
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
        order = await database.fetch_one(query_order, {"orderid": refund_request.orderid})

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Check if the order is eligible for a refund (e.g., no deliveries completed, within refund period)
        query_delivery_status = 
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
            SELECT status
            FROM deliveries
            WHERE orderid = :orderid
        
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
        delivery = await database.fetch_one(query_delivery_status, {"orderid": refund_request.orderid})

        if delivery and delivery["status"] == "Completed":
            raise HTTPException(status_code=400, detail="Refund cannot be processed for completed deliveries")

        # Process the refund by marking the order as refunded and updating stock
        async with database.transaction():
            # Update order status
            update_order_query = 
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
                UPDATE orders
                SET status = 'Refunded'
                WHERE orderid = :orderid
            
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
            await database.execute(update_order_query, {"orderid": refund_request.orderid})

            # Restore stock for refunded items
            query_order_items = 
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
                SELECT productid, quantity
                FROM order_items
                WHERE orderid = :orderid
            
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
            order_items = await database.fetch_all(query_order_items, {"orderid": refund_request.orderid})

            for item in order_items:
                restore_stock_query = 
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
                    UPDATE products
                    SET stock = stock + :quantity
                    WHERE productid = :productid
                
        # Check if the order is within the 30-day refund period
        query_order_date = """
            SELECT order_date
            FROM orders
            WHERE orderid = :orderid
        """
        order_date = await database.fetch_one(query_order_date, {"orderid": refund_request.orderid})
        if not order_date:
            raise HTTPException(status_code=404, detail="Order date not found")

        max_refund_date = order_date["order_date"] + timedelta(days=30)
        if datetime.now() > max_refund_date:
            raise HTTPException(status_code=400, detail="Refund request exceeds the 30-day period")

        
                await database.execute(restore_stock_query, {
                    "quantity": item["quantity"],
                    "productid": item["productid"]
                })

        # Return the refund response
        return RefundResponse(
            orderid=refund_request.orderid,
            refunded_amount=order["total_amount"],
            status="Refunded"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the refund: {str(e)}")

