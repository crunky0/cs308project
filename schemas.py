# schemas.py
from pydantic import BaseModel
from typing import Optional

# Product creation/update
class ProductCreate(BaseModel):
    serialnumber: Optional[int]
    productname: str
    productmodel: str
    description: str
    distributerinfo: str
    warranty: str
    price: float
    stock: int
    categoryid: int

class ProductStockUpdate(BaseModel):
    stock: int

# Review approval update
class ReviewUpdate(BaseModel):
    approved: bool

# (Optional) Delivery status update
class DeliveryStatusUpdate(BaseModel):
    status: str

# Invoice read schema
class InvoiceRead(BaseModel):
    invoiceid: int
    orderid: int
    invoice_number: str
    file_path: str

    class Config:
        orm_mode = True

# (Optional) Delivery read schema
class DeliveryRead(BaseModel):
    deliveryid: int
    orderid: int
    status: str

    class Config:
        orm_mode = True
