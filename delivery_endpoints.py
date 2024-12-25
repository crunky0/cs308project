
from fastapi import APIRouter, Depends, HTTPException, status
from databases import Database
from db import database
from pydantic import BaseModel
from datetime import datetime
from dependencies import product_manager_required
from models import User

class DeliveryCreate(BaseModel):
    orderid: int
    status: str

class DeliveryUpdate(BaseModel):
    status: str

class DeliveryRead(BaseModel):
    deliveryid: int
    orderid: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # or "orm_mode=True" in Pydantic v1
        

router = APIRouter()



# 3) Get a single delivery
@router.get("/deliveries/{deliveryid}", response_model=DeliveryRead)
async def get_delivery(
    deliveryid: int,
    current_user: User = Depends(product_manager_required)
):
    query = """
        SELECT deliveryid, orderid, status, created_at
        FROM deliveries
        WHERE deliveryid = :did
    """
    row = await database.fetch_one(query, {"did": deliveryid})
    if not row:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return DeliveryRead(**dict(row))

# 5) (Optional) Delete a delivery
@router.delete("/deliveries/{deliveryid}/delete", response_model=dict)
async def delete_delivery(
    deliveryid: int,
    current_user: User = Depends(product_manager_required)
):
    # Check if it exists
    row = await database.fetch_one("SELECT deliveryid FROM deliveries WHERE deliveryid = :did", {"did": deliveryid})
    if not row:
        raise HTTPException(status_code=404, detail="Delivery not found")

    await database.execute("DELETE FROM deliveries WHERE deliveryid = :did", {"did": deliveryid})
    return {"detail": "Delivery deleted successfully"}
