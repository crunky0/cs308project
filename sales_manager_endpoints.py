from fastapi import APIRouter, HTTPException,Query
from pydantic import BaseModel, Field
from typing import List
from db import database
from mailing_service import MailingService
from datetime import datetime
import os
from fastapi.responses import FileResponse

# Initialize router and mailing service
router = APIRouter()
mailing_service = MailingService()

# Pydantic models for request validation
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

class RevenueProfitLossChart(BaseModel):
    date: str
    revenue: float
    profit_loss: float


# Set product price
@router.put("/set_price")
async def set_price(update: PriceUpdate):
    query = "UPDATE products SET price = :new_price WHERE productid = :productid"
    values = {"productid": update.productid, "new_price": update.new_price}
    await database.execute(query, values)
    return {"message": "Price updated successfully"}

@router.put("/set_discounts_and_notify")
async def set_discounts_and_notify(updates: List[DiscountUpdate]):
    """
    Apply discounts to multiple products and notify users with those products in their wishlist.
    """
    try:
        # Step 1: Update discount prices for all specified products
        for update in updates:
            query = "UPDATE products SET discountprice = :discount_price WHERE productid = :productid"
            await database.execute(query, {"productid": update.productid, "discount_price": update.discount_price})

        # Step 2: Fetch all users with discounted products in their wishlist
        product_ids = [update.productid for update in updates]
        wishlist_query = f"""
        SELECT u.userid, u.email, u.name, p.productname, p.price, p.discountprice
        FROM wishlist w
        JOIN users u ON w.userid = u.userid
        JOIN products p ON w.productid = p.productid
        WHERE p.productid IN ({','.join(map(str, product_ids))});
        """
        users = await database.fetch_all(wishlist_query)

        if not users:
            return {"message": "Discounts applied successfully, but no users to notify."}

        # Step 3: Aggregate discounted products per user
        user_notifications = {}
        for user in users:
            userid = user["userid"]
            if userid not in user_notifications:
                user_notifications[userid] = {
                    "email": user["email"],
                    "name": user["name"],
                    "products": []
                }
            user_notifications[userid]["products"].append({
                "productname": user["productname"],
                "original_price": user["price"],
                "discounted_price": user["discountprice"]
            })

        # Step 4: Notify each user about all discounted products in their wishlist
        for user_data in user_notifications.values():
            email = user_data["email"]
            name = user_data["name"]
            products = user_data["products"]

            # Construct email body
            product_details = "".join([
                f"<p><strong>{product['productname']}</strong><br>"
                f"Original Price: ${product['original_price']:.2f}<br>"
                f"Discounted Price: ${product['discounted_price']:.2f}</p>"
                for product in products
            ])
            email_body = f"""
            <html>
            <body>
                <p>Dear {name},</p>
                <p>Good news! The following products from your wishlist are now available at discounted prices:</p>
                {product_details}
                <p>Don't miss out on these deals! Visit our store to purchase them now.</p>
                <p>Best regards,<br>Your CS308 Team</p>
            </body>
            </html>
            """

            # Send email
            mailing_service.send_email(
                recipient_email=email,
                subject="Discount Alert: Wishlist Products",
                body=email_body,
            )

        return {"message": "Discounts applied successfully and users notified."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

INVOICE_DIR = "invoices/"  # Directory where invoice PDFs are stored

# Fetch invoices in a given date range
@router.get("/invoices")
async def fetch_invoices(start_date: datetime, end_date: datetime) -> List[str]:
    """
    Fetch a list of invoice file names generated within a given date range.
    """
    try:
        if not os.path.exists(INVOICE_DIR):
            raise HTTPException(status_code=404, detail="Invoice directory not found")

        # List all files in the invoice directory
        all_files = os.listdir(INVOICE_DIR)
        invoices_in_range = []

        # Filter files by date range
        for file_name in all_files:
            try:
                # Extract timestamp from the file name (e.g., "INV-20231225120000.pdf")
                timestamp_str = file_name.split("-")[1].replace(".pdf", "")
                file_date = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")

                if start_date <= file_date <= end_date:
                    invoices_in_range.append(file_name)
            except Exception:
                continue  # Skip files that do not match the expected naming format

        return invoices_in_range
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Download a specific invoice
@router.get("/invoices/{invoice_name}")
async def download_invoice(invoice_name: str):
    """
    Download a specific invoice file by its name.
    """
    try:
        # Construct the full file path
        file_path = os.path.join(INVOICE_DIR, invoice_name)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Invoice file not found")

        # Return the file for download using FileResponse
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=invoice_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profit_loss_chart", response_model=List[RevenueProfitLossChart])
async def get_revenue_and_profit_loss_chart(
    start_date: datetime = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(..., description="End date in YYYY-MM-DD format"),
):
    """
    Calculates revenue and profit/loss for each day in a given date range.
    Returns the results grouped by date for chart rendering.
    """
    try:
        # Validate date range
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")

        # Query to calculate revenue and profit/loss grouped by orderdate
        query = """
            SELECT 
                DATE(o.orderdate) AS date,
                SUM(oi.quantity * 
                    CASE 
                        WHEN p.discountprice IS NOT NULL THEN p.discountprice 
                        ELSE p.price 
                    END
                ) AS revenue,
                SUM(
                    (CASE 
                        WHEN p.discountprice IS NOT NULL THEN p.discountprice 
                        ELSE p.price 
                     END - p.cost) * oi.quantity
                ) AS profit_loss
            FROM orders o
            JOIN order_items oi ON o.orderid = oi.orderid
            JOIN products p ON oi.productid = p.productid
            WHERE o.orderdate BETWEEN :start_date AND :end_date
            GROUP BY DATE(o.orderdate)
            ORDER BY DATE(o.orderdate)
        """

        rows = await database.fetch_all(query, {"start_date": start_date, "end_date": end_date})

        # Format results for the chart
        return [
            {
                "date": row["date"].isoformat(),
                "revenue": float(row["revenue"]),
                "profit_loss": float(row["profit_loss"]),
            }
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
