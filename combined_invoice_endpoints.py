from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from order_service import OrderService
from services.invoice_service import InvoiceService
from mailing_service import MailingService
from db import database  # Import the database connection
from datetime import datetime

# Define your Order Item request model
class OrderItemRequest(BaseModel):
    productid: int
    quantity: int
    price: float
    productname: str

class OrderRequest(BaseModel):
    userid: int
    totalamount: float
    items: List[OrderItemRequest]

# Initialize services
order_service = OrderService(database)  # Use the database connection
invoice_service = InvoiceService(output_dir="invoices")
mailing_service = MailingService()

# Create the router
router = APIRouter()

@router.post("/create_order_with_invoice")
async def create_order_with_invoice(order_data: OrderRequest):
    try:
        # Step 1: Create the order
        order_response = await order_service.create_order(order_data.dict())
        orderid = order_response["orderid"]

        # Step 2: Fetch user details (name, email, homeaddress)
        user = await database.fetch_one("""
            SELECT name, email, homeaddress
            FROM users
            WHERE userid = :userid
        """, {"userid": order_data.userid})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        email = user["email"]
        user_name = user["name"]
        homeaddress = user["homeaddress"]

        # Step 3: Generate the invoice HTML
        invoice_number = f"INV-{orderid}"  # Use order ID in invoice number
        invoice_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = [
            {"name": item.productname, "quantity": item.quantity, "price": item.price}
            for item in order_data.items
        ]
        invoice_html = invoice_service._create_invoice_html(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            user_info={"name": user_name, "email": email, "homeaddress": homeaddress},
            items=items,
            total_amount=order_data.totalamount,
        )

        # Step 4: Generate the invoice PDF
        invoice_file_path = invoice_service.generate_invoice(
            html_content=invoice_html,
            invoice_number=invoice_number,
        )

        # Step 5: Send the invoice via email
        mailing_service.send_invoice_email(email, invoice_file_path)

        # Step 6: Return the invoice HTML
        return {"message": "Order created successfully", "orderid": orderid, "invoice_html": invoice_html}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
