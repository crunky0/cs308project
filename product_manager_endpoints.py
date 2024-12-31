# product_manager_endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.responses import FileResponse
from dependencies import  product_manager_required
from pydantic import BaseModel
from invoice_endpoints import InvoiceRequest
from product_endpoints import ProductCreate
from db import database
from datetime import datetime
import os
from typing import Literal
from datetime import date

class DeliveryCreate(BaseModel):
    orderid: int
    
class DeliveryUpdate(BaseModel):
    status: str

class DeliveryRead(BaseModel):
    deliveryid: int
    orderid: int
    customerid: int
    productid: int
    quantity: int
    total_price: float
    delivery_address: str
    status: Literal['processing', 'in-transit', 'delivered']  # Updated to reflect the `status` column
    orderdate: date  # Added to include `orderdate`
    price: float  # Added to include `price`
    
# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()

manager_router = APIRouter(
    prefix="/productmanagerpanel",
    tags=["product_manager_panel"]
)

#####################
#   CATEGORY
#####################

@manager_router.post("/categories")
async def add_category(
    category_data: str,
    current_user_id: int = Depends(product_manager_required),

):
    query = """
        INSERT INTO categories (name)
        VALUES (:name)
        RETURNING categoryid
    """
    values = {"name": category_data}
    categoryid = await database.fetch_val(query, values)
    return {"detail": "Category added successfully", "categoryid": categoryid}

@manager_router.delete("/categories/{category_id}")
async def remove_category(
    category_id: int,
    current_user_id: int = Depends(product_manager_required),
  
):
    # check if exists
    check_query = "SELECT categoryid FROM categories WHERE categoryid = :cat_id"
    row = await database.fetch_one(check_query, {"cat_id": category_id})
    if not row:
        raise HTTPException(status_code=404, detail="Category not found")

    delete_query = "DELETE FROM categories WHERE categoryid = :cat_id"
    await database.execute(delete_query, {"cat_id": category_id})
    return {"detail": "Category removed successfully"}

#####################
#   PRODUCTS
#####################

@manager_router.post("/products")
async def add_product(
    product_data: ProductCreate,
    current_user_id: int = Depends(product_manager_required),
   
):
    query = load_sql_file("add_product.sql")
    values = product_data.dict()
    productid = await database.fetch_val(query, values)
    return {"detail": "Product added successfully", "product_id": productid}

@manager_router.delete("/products/{product_id}")
async def remove_product(
    product_id: int,
    current_user_id: int = Depends(product_manager_required),

):
    query = load_sql_file("find_product.sql")
    row = await database.fetch_one(query, {"productID": product_id})
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_query = load_sql_file("remove_product.sql")
    await database.execute(delete_query, {"productID": product_id})
    return {"detail": "Product removed successfully"}

@manager_router.patch("/products/{productid}/stock")
async def update_product_stock(
    productid: int,
    stock: int,
    #current_user_id: int = Depends(product_manager_required),
 
):
    # check product
    query = load_sql_file("find_product.sql")
    product_row = await database.fetch_one(query, {"productID": productid})
    if not product_row:
        raise HTTPException(status_code=404, detail="Product not found")

    update_query = """
        UPDATE products
        SET stock = :stock
        WHERE productid = :productid
    """
    await database.execute(update_query, {"stock": stock, "productid": productid})
    return {"detail": "Stock updated successfully", "new_stock": stock}

#####################
#   DELIVERIES
#####################

@manager_router.get("/deliveries")
async def view_deliveries(
):
    query = load_sql_file("get_all_deliveries.sql")
    rows = await database.fetch_all(query)
    deliveries = [dict(row) for row in rows]
    return {"deliveries": deliveries}

@manager_router.patch("/orders/{orderid}/status")
async def update_order_status(
    orderid: int,
    status: str
):
    """
    Update the status of an order and its associated deliveries to either 'in-transit' or 'delivered'.
    """

    # Validate status
    if status not in ["in-transit", "delivered"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'in-transit' or 'delivered'.")

    # Check if the order exists
    check_order_query = "SELECT orderid FROM orders WHERE orderid = :oid"
    order = await database.fetch_one(check_order_query, {"oid": orderid})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the order's status
    update_order_query = """
        UPDATE orders
        SET status = :status
        WHERE orderid = :oid
    """
    await database.execute(update_order_query, {"oid": orderid, "status": status})

    # Update all associated deliveries' status
    update_deliveries_query = """
        UPDATE deliveries
        SET status = :status
        WHERE orderid = :oid
    """
    await database.execute(update_deliveries_query, {"oid": orderid, "status": status})

    return {"detail": f"Order and associated deliveries marked as {status}"}

@manager_router.post("/deliveries/create", response_model=List[DeliveryRead])
async def create_delivery(
    delivery_data: DeliveryCreate
):
    """
    Use the SQL script in `add_delivery.sql` to insert rows into `deliveries` and return the created rows.
    """

    # Load the SQL script
    insert_query = load_sql_file("add_delivery.sql")

    # Execute the query and fetch all newly inserted rows
    try:
        new_rows = await database.fetch_all(insert_query, {"oid": delivery_data.orderid})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create delivery: {str(e)}")

    if not new_rows:
        raise HTTPException(status_code=400, detail="No deliveries were created")

    # Return the inserted deliveries as a response
    return [DeliveryRead(**dict(row)) for row in new_rows]

@manager_router.get("/orders/processing")
async def get_processing_orders():
    """
    Retrieve all orders with the status of 'processing', including their items.
    """

    # Query to get all orders with status 'processing'
    orders_query = """
        SELECT *
        FROM orders
        WHERE status = 'processing';
    """

    # Query to get items for a specific order
    items_query = """
        SELECT productid, quantity
        FROM order_items
        WHERE orderid = :orderid;
    """

    # Fetch all orders with status 'processing'
    orders = await database.fetch_all(orders_query)

    # Add items to each order
    results = []
    for order in orders:
        items = await database.fetch_all(items_query, {"orderid": order["orderid"]})
        results.append({
            "orderid": order["orderid"],
            "userid": order["userid"],
            "totalamount": order["totalamount"],
            "orderdate": order["orderdate"],
            "status": order["status"],
            "items": [
                {
                    "productid": item["productid"],
                    "quantity": item["quantity"]
                } for item in items
            ]
        })

    return results





#####################
#   INVOICES
#####################

@manager_router.get("/invoices", response_model=List[str])
async def list_invoices(current_user_id: int = Depends(product_manager_required)):
    """
    Return a list of all invoice PDF filenames in the 'invoices' folder.
    """
    folder_path = "invoices"
    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="Invoices folder not found")

    # List all PDF files
    invoice_files = [
        file_name for file_name in os.listdir(folder_path)
        if file_name.lower().endswith(".pdf")
    ]
    return invoice_files

@manager_router.get("/invoices/{filename}", response_class=FileResponse)
async def get_invoice(
    filename: str,
    current_user_id: int = Depends(product_manager_required)
):
    """
    Return the requested invoice PDF file from the 'invoices' folder.
    """
    file_path = os.path.join("invoices", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Invoice not found")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )

#####################
#   REVIEWS
#####################

@manager_router.patch("/reviews/{review_id}")
async def approve_or_disapprove_review(
    review_id: int,
    approved: bool,  # <-- new direct boolean parameter
    current_user_id: int = Depends(product_manager_required),
):
    # 1) Check if review exists
    check_query = "SELECT reviewid FROM ratings WHERE reviewid = :rid"
    row = await database.fetch_one(check_query, {"rid": review_id})
    if not row:
        raise HTTPException(status_code=404, detail="Review not found")

    # 2) Update the 'approved' field (TRUE/FALSE)
    update_query = """
        UPDATE ratings
        SET approved = :approved
        WHERE reviewid = :rid
    """
    await database.execute(update_query, {"approved": approved, "rid": review_id})

    status_str = "approved" if approved else "disapproved"
    return {"detail": f"Review {status_str} successfully"}

        