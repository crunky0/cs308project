from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from databases import Database

# Initialize router
router = APIRouter()

# Pydantic model for refund request
class RefundRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

from db import database

@router.post("/refund/request")
async def request_refund(refund: RefundRequest):
    purchase_query = """
    SELECT * FROM card 
    WHERE user_id = :user_id AND product_id = :product_id
    """
    purchase = await database.fetch_one(query=purchase_query, values={"user_id": refund.user_id, "product_id": refund.product_id})
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found for this user and product.")

    if refund.quantity > purchase["quantity"]:
        raise HTTPException(status_code=400, detail="Refund quantity exceeds the purchased quantity.")

    update_stock_query = """
    UPDATE products SET stock = stock + :quantity WHERE productid = :product_id
    """
    await database.execute(query=update_stock_query, values={"quantity": refund.quantity, "product_id": refund.product_id})

    update_card_query = """
    UPDATE card SET quantity = quantity - :quantity 
    WHERE user_id = :user_id AND product_id = :product_id
    """
    await database.execute(query=update_card_query, values={"quantity": refund.quantity, "user_id": refund.user_id, "product_id": refund.product_id})

    delete_empty_card_query = """
    DELETE FROM card WHERE user_id = :user_id AND product_id = :product_id AND quantity = 0
    """
    await database.execute(query=delete_empty_card_query, values={"user_id": refund.user_id, "product_id": refund.product_id})

    return {
        "message": "Refund processed successfully.",
        "details": {
            "product_id": refund.product_id,
            "user_id": refund.user_id,
            "quantity_refunded": refund.quantity
        }
    }
