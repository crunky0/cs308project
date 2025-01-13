from fastapi import APIRouter, HTTPException,Query
from pydantic import BaseModel, Field
from typing import List,Dict,Any
from db import database
from mailing_service import MailingService
from datetime import datetime
import os
from fastapi.responses import FileResponse
from refund_process import RefundService  
from refund_endpoint import RefundRequest, RefundDecision ,RefundResponse
from matplotlib import pyplot as plt
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
    discount_price: float = Field(default=None, gt=0, description="Manually calculated discounted price ")
    discount_rate: float = Field(default=None, gt=0, lt=100, description="Discount rate as a percentage ")


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
    """
    Update the price of a product and automatically adjust its cost to 50% of the new price.
    """
    try:
        # Calculate the cost as 50% of the new price
        new_cost = update.new_price * 0.5

        # Update both price and cost in the database
        query = """
        UPDATE products 
        SET price = :new_price, 
            cost = :new_cost 
        WHERE productid = :productid
        """
        values = {"productid": update.productid, "new_price": update.new_price, "new_cost": new_cost}
        await database.execute(query, values)

        return {"message": "Price and cost updated successfully", "new_price": update.new_price, "new_cost": new_cost}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update price and cost: {str(e)}")


@router.put("/set_discounts_and_notify")
async def set_discounts_and_notify(updates: List[DiscountUpdate]):
    """
    Apply discounts to multiple products and notify users with those products in their wishlist.
    """
    try:
        for update in updates:
            # Validate input: either `discount_rate` or `discount_price` must be provided, but not both
            if update.discount_rate is None and update.discount_price is None:
                raise HTTPException(
                    status_code=400,
                    detail="Either discount_rate or discount_price must be provided."
                )
            if update.discount_rate is not None and update.discount_price is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Provide either discount_rate or discount_price, not both."
                )

            # Fetch the product price for rate-based discount calculation
            if update.discount_rate is not None:
                query = "SELECT price FROM products WHERE productid = :productid"
                product = await database.fetch_one(query, {"productid": update.productid})
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product ID {update.productid} not found.")

                # Cast `price` to `float` for calculations
                product_price = float(product["price"])
                
                # Calculate discounted price
                calculated_discount_price = product_price * (1 - update.discount_rate / 100)
            else:
                # Use the manually provided `discount_price`
                calculated_discount_price = update.discount_price


            # Update the product with the calculated discount price
            update_query = "UPDATE products SET discountprice = :discount_price WHERE productid = :productid"
            await database.execute(update_query, {"productid": update.productid, "discount_price": calculated_discount_price})

        # Fetch and notify users about the discounts
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

        # Aggregate notifications by user
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

        # Notify users
        for user_data in user_notifications.values():
            email = user_data["email"]
            name = user_data["name"]
            products = user_data["products"]

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


@router.get("/profit_loss_chart_image")
async def generate_profit_loss_chart_image(
    start_date: datetime = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(..., description="End date in YYYY-MM-DD format"),
):
    """
    Generate a chart of revenue and profit/loss for the given date range and save it in the `charts` directory.
    The filename will be based on the date range provided.
    """
    try:
        # Step 1: Validate date range
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")

        # Step 2: Fetch data from the database
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

        if not rows:
            raise HTTPException(status_code=404, detail="No data found for the given date range.")

        # Step 3: Prepare data for the chart
        dates = [row["date"] for row in rows]
        revenue = [row["revenue"] for row in rows]
        profit_loss = [row["profit_loss"] for row in rows]

        # Step 4: Generate the chart
        plt.figure(figsize=(10, 6))
        plt.plot(dates, revenue, label="Revenue", marker="o", color="blue")
        plt.plot(dates, profit_loss, label="Profit/Loss", marker="x", color="green")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Revenue and Profit/Loss Over Time")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Step 5: Save the chart in the `charts` directory
        chart_directory = "charts"
        os.makedirs(chart_directory, exist_ok=True)  # Ensure the directory exists

        # Generate a filename based on the date range
        chart_filename = f"chart_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.png"
        chart_path = os.path.join(chart_directory, chart_filename)

        plt.savefig(chart_path)
        plt.close()

        # Step 6: Return the saved chart path
        return FileResponse(chart_path, media_type="image/png", filename=chart_filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/refunds/pending", response_model=List[Dict[str, int]])
async def view_pending_refunds():
    """
    View all pending refund requests.
    """
    try:
        query = """
            SELECT orderid, productid, quantity
            FROM refund_requests
        """
        refunds = await database.fetch_all(query)
        return [dict(refund) for refund in refunds]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending refunds: {str(e)}")
refund_service = RefundService(database)

@router.post("/refunds/process", response_model=Dict[str, str])
async def process_refund(decision: RefundDecision):
    """
    Process a refund request (approve or deny).
    """
    try:
        if decision.approved:
            # Approve the refund and update stock
            await refund_service.process_refund(decision.orderid)
            return {"message": "Refund approved successfully."}
        else:
            # Deny the refund and remove the request
            query = """
                DELETE FROM refund_requests
                WHERE orderid = :orderid
            """
            await database.execute(query, {"orderid": decision.orderid})
            return {"message": "Refund denied successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process refund: {str(e)}")

@router.post("/refund/decision", response_model=RefundResponse)
async def manager_decision(decision: RefundDecision):
    """
    Endpoint for the Sales Manager to evaluate and process a refund decision.
    """
    try:
        if decision.approved:
            # Fetch pending refund request details for the order
            query = """
                SELECT productid, quantity
                FROM refund_requests
                WHERE orderid = :orderid
            """
            product_quantities = await database.fetch_all(query, {"orderid": decision.orderid})
            
            if not product_quantities:
                raise HTTPException(status_code=404, detail="No refund request found for this order.")
            
            # Convert to a list of dictionaries
            product_quantities = [dict(product) for product in product_quantities]

            # Process the refund
            refunded_amount = await refund_service.process_refund(decision.orderid, product_quantities)

            # Notify the customer via email
            user_info = await database.fetch_one(
                "SELECT name, email FROM users WHERE userid = (SELECT userid FROM orders WHERE orderid = :orderid)",
                {"orderid": decision.orderid},
            )
            if not user_info:
                raise HTTPException(status_code=404, detail="User not found")

            email_subject = f"Refund Processed for Order #{decision.orderid}"

            email_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        background-color: #f9f9f9;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: #ffffff;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .header h1 {{
                        font-size: 24px;
                        color: #4CAF50;
                    }}
                    .content p {{
                        margin: 10px 0;
                        color: #555;
                    }}
                    .content ul {{
                        padding-left: 20px;
                    }}
                    .content ul li {{
                        margin-bottom: 10px;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        font-size: 12px;
                        color: #999;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 10px 20px;
                        margin: 20px 0;
                        color: #ffffff;
                        background-color: #4CAF50;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .button:hover {{
                        background-color: #45a049;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Header Section -->
                    <div class="header">
                        <h1>Refund Confirmation</h1>
                    </div>

                    <!-- Content Section -->
                    <div class="content">
                        <p>Dear <strong>{user_info['name']}</strong>,</p>

                        <p>We are pleased to inform you that your refund request for <strong>Order #{decision.orderid}</strong> has been successfully approved. Below are the details of your refund:</p>

                        <ul>
                            <li><strong>Order Number:</strong> #{decision.orderid}</li>
                            <li><strong>Refunded Amount:</strong> ${refunded_amount:.2f}</li>
                            <li><strong>Refund Processed Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</li>
                        </ul>

                        <p>The refunded amount has been credited to the original payment method you used at the time of purchase. Please allow 3–5 business days for the amount to reflect in your account, depending on your financial institution's processing time.</p>

                        <p>If you have any questions regarding your refund, feel free to contact our support team. We are always happy to assist you!</p>

                        <!-- Call to Action Button -->
                        <a href="https://yourstore.example.com/support" class="button">Contact Support</a>
                    </div>

                    <!-- Footer Section -->
                    <div class="footer">
                        <p>Thank you for shopping with us!</p>
                        <p><em>Your Store Team</em></p>
                        <p>For more information, visit our <a href="https://yourstore.example.com">website</a>.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            mailing_service.send_email(user_info["email"], email_subject, email_body)

            return RefundResponse(
                orderid=decision.orderid,
                refunded_amount=refunded_amount,
                status="Refunded",
            )
        else:
            # Deny refund logic
            await refund_service.deny_refund(decision.orderid)

            # Notify the customer about the denial
            user_info = await database.fetch_one(
                "SELECT name, email FROM users WHERE userid = (SELECT userid FROM orders WHERE orderid = :orderid)",
                {"orderid": decision.orderid},
            )
            if not user_info:
                raise HTTPException(status_code=404, detail="User not found")

            email_subject = f"Refund Processed for Order {decision.orderid}"
            email_body = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Refund Processed</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f9f9f9;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        padding: 10px 0;
                        border-bottom: 2px solid #4CAF50;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                        color: #4CAF50;
                    }}
                    .content {{
                        margin: 20px 0;
                    }}
                    .content p {{
                        margin: 8px 0;
                        line-height: 1.6;
                    }}
                    .table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    .table th, .table td {{
                        border: 1px solid #ddd;
                        padding: 10px;
                        text-align: left;
                    }}
                    .table th {{
                        background-color: #f2f2f2;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        font-size: 14px;
                        color: #777;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Refund Confirmation</h1>
                    </div>
                    <div class="content">
                        <p>Dear <strong>{user_name}</strong>,</p>
                        <p>Your refund request for <strong>Order #{decision.orderid}</strong> has been successfully processed. Here are the details of the refund:</p>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Quantity</th>
                                    <th>Refunded Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join(f"<tr><td>{product['productname']}</td><td>{product['quantity']}</td><td>${product['price']:.2f}</td></tr>" for product in products)}
                            </tbody>
                        </table>
                        <p><strong>Total Refunded Amount:</strong> ${refunded_amount:.2f}</p>
                        <p>Refunded to your account: <strong>{email}</strong></p>
                    </div>
                    <div class="footer">
                        <p>Thank you for shopping with us!</p>
                        <p><em>Your Store Team</em></p>
                    </div>
                </div>
            </body>
            </html>
            """
            mailing_service.send_email(user_info["email"], email_subject, email_body)

            return RefundResponse(
                orderid=decision.orderid,
                refunded_amount=0.0,
                status="Denied",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
