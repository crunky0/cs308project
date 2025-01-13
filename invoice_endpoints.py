from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.invoice_service import InvoiceService
from datetime import datetime

# Initialize the router and InvoiceService
router = APIRouter()
invoice_service = InvoiceService()

# Pydantic models for request validation
class UserInfo(BaseModel):
    name: str
    email: str
    homeaddress: str  # Added to include user address in the invoice

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class InvoiceRequest(BaseModel):
    orderid: int  # Added to use orderid for naming invoices
    user_info: UserInfo
    items: List[Item]
    total_amount: float

@router.post("/generate-invoice")
async def generate_invoice(request: InvoiceRequest):
    try:
        # Use orderid for invoice number
        invoice_number = f"INV-{request.orderid}"
        invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create HTML content for the invoice, including the home address
        html_content = invoice_service._create_invoice_html(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            user_info=request.user_info.dict(),
            items=[item.dict() for item in request.items],
            total_amount=request.total_amount
        )

        # Generate the PDF invoice using the updated naming convention
        file_path = invoice_service.generate_invoice(html_content, invoice_number)
        return {"message": "Invoice generated successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
