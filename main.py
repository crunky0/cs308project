from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,  Extra
from services.invoice_service import InvoiceService
from typing import List

app = FastAPI()

# Pydantic model for the request body

class UserInfo(BaseModel):
    name: str
    email: str


    class Config:
        extra = 'forbid'  # Forbid extra fields


class Item(BaseModel):
    name: str
    quantity: int
    price: float

class InvoiceRequest(BaseModel):
    user_info: UserInfo
    items: List[Item]
    total_amount: float

# Initialize the InvoiceService
invoice_service = InvoiceService()

@app.post("/generate-invoice")
async def generate_invoice(request: InvoiceRequest):
    try:
        # Convert Pydantic models to dictionaries
        user_info_dict = request.user_info.model_dump()  # Convert UserInfo to dict
        items_list_dict = [item.model_dump() for item in request.items]  # Convert each Item to dict

        # Call the InvoiceService to generate the invoice
        file_path = invoice_service.generate_invoice(
            user_info=user_info_dict,
            items=items_list_dict,
            total_amount=request.total_amount
        )
        return {"message": "Invoice generated successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
