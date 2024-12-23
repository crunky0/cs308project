# schemas.py
from pydantic import BaseModel
from typing import Optional

# Category
class CategoryCreate(BaseModel):
    name: str

# Product
class ProductCreate(BaseModel):
    categoryid: int
    productname: str
    productmodel: str
    description: str
    distributerinfo: Optional[str] = None
    warranty: Optional[str] = None
    price: float
    stock: int

class ProductStockUpdate(BaseModel):
    stock: int

# Review
class ReviewApproval(BaseModel):
    approved: bool

# Delivery
class DeliveryUpdate(BaseModel):
    completed: bool

# Invoice (to list them)
class InvoiceRead(BaseModel):
    invoiceid: int
    orderid: int
    invoice_number: str
    file_path: Optional[str] = None

    # Pydantic v2: "from_attributes" instead of "orm_mode"
    class Config:
        from_attributes = True

