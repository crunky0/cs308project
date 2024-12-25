from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from db import database

router = APIRouter()

class PriceUpdate(BaseModel):
    productid: int
    new_price: float = Field(gt=0, description="Price must be greater than 0")

class DiscountUpdate(BaseModel):
    productid: int
    discount_price: float = Field(gt=0, description="Discount must be greater than 0")

class CostUpdate(BaseModel):
    productid: int
    new_cost: float = Field(gt=0, description="Cost must be greater than 0")

class ProfitLossReport(BaseModel):
    productid: int
    profit_loss: float

# Set product price
@router.put("/set_price")
async def set_price(update: PriceUpdate):
    query = "UPDATE products SET price = :new_price WHERE productid = :productid"
    values = {"productid": update.productid, "new_price": update.new_price}
    await database.execute(query, values)
    return {"message": "Price updated successfully"}

# Set product discount
@router.put("/set_discount")
async def set_discount(update: DiscountUpdate):
    query = "UPDATE products SET discountprice = :discount_price WHERE productid = :productid"
    values = {"productid": update.productid, "discount_price": update.discount_price}
    await database.execute(query, values)
    return {"message": "Discount updated successfully"}

# Set product cost
@router.put("/set_cost")
async def set_cost(update: CostUpdate):
    query = "UPDATE products SET cost = :new_cost WHERE productid = :productid"
    values = {"productid": update.productid, "new_cost": update.new_cost}
    await database.execute(query, values)
    return {"message": "Cost updated successfully"}

# Get profit/loss report considering discount
@router.get("/profit_loss_report", response_model=List[ProfitLossReport])
async def get_profit_loss_report():
    """
    Calculates profit or loss for each product, considering discounts if applicable.
    """
    query = """
        SELECT 
            productid, 
            SUM(CASE 
                WHEN discountprice IS NOT NULL 
                THEN discountprice * soldamount
                ELSE price * soldamount 
            END) - (cost * soldamount) AS profit_loss
        FROM products
        GROUP BY productid
    """
    rows = await database.fetch_all(query)
    return [{"productid": row["productid"], "profit_loss": row["profit_loss"]} for row in rows]
