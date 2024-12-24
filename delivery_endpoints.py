
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

# 1) Create a new delivery
@router.post("/deliveries/create", response_model=DeliveryRead, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    delivery_data: DeliveryCreate,  # or a session if you're using session-based
    current_user: User = Depends(product_manager_required)  # if restricted to certain role
):
    # Insert into DB
    insert_query = """
        INSERT INTO deliveries (orderid, status)
        VALUES (:orderid, :status)
        RETURNING deliveryid, orderid, status, created_at
    """
    values = {
        "orderid": delivery_data.orderid,
        "status": delivery_data.status
    }
    row = await database.fetch_one(insert_query, values)
    if not row:
        raise HTTPException(status_code=400, detail="Failed to create delivery")

    return DeliveryRead(**dict(row))

# 2) List all deliveries
@router.get("/deliveries", response_model=list[DeliveryRead])
async def list_deliveries(

    current_user: User = Depends(product_manager_required)
):
    query = """
        SELECT deliveryid, orderid, status, created_at
        FROM deliveries
        ORDER BY deliveryid
    """
    rows = await database.fetch_all(query)
    return [DeliveryRead(**dict(r)) for r in rows]

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

# 4) Update delivery status
@router.patch("/deliveries/{deliveryid}/update", response_model=DeliveryRead)
async def update_delivery_status(
    deliveryid: int,
    update_data: DeliveryUpdate,
    current_user: User = Depends(product_manager_required)
):
    # First check if it exists
    check_query = "SELECT deliveryid, orderid, status, created_at FROM deliveries WHERE deliveryid = :did"
    existing = await database.fetch_one(check_query, {"did": deliveryid})
    if not existing:
        raise HTTPException(status_code=404, detail="Delivery not found")

    update_query = """
        UPDATE deliveries
        SET status = :status
        WHERE deliveryid = :did
        RETURNING deliveryid, orderid, status, created_at
    """
    row = await database.fetch_one(update_query, {"status": update_data.status, "did": deliveryid})
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
