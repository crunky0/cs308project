from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from services.invoice_service import InvoiceService
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Initialize InvoiceService
invoice_service = InvoiceService()

# Pydantic models for request validation
class UserInfo(BaseModel):
    name: str
    email: str

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class InvoiceRequest(BaseModel):
    user_info: UserInfo
    items: List[Item]
    total_amount: float

@app.post("/generate-invoice")
async def generate_invoice(request: InvoiceRequest):
    try:
        # Generate unique invoice number and date
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create HTML content for the invoice
        html_content = invoice_service._create_invoice_html(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            user_info=request.user_info.dict(),
            items=[item.dict() for item in request.items],
            total_amount=request.total_amount
        )

        # Generate the PDF invoice
        file_path = invoice_service.generate_invoice(html_content, invoice_number)
        return {"message": "Invoice generated successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
