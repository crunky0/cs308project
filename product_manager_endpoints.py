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

class DeliveryCreate(BaseModel):
    orderid: int
    delivery_address: str
    
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
    completed: bool
    
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

@manager_router.patch("/products/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    stock: int,
    current_user_id: int = Depends(product_manager_required),
 
):
    # check product
    query = load_sql_file("find_product.sql")
    product_row = await database.fetch_one(query, {"productID": product_id})
    if not product_row:
        raise HTTPException(status_code=404, detail="Product not found")

    update_query = """
        UPDATE products
        SET stock = :stock
        WHERE productid = :pid
    """
    await database.execute(update_query, {"stock": stock, "pid": product_id})
    return {"detail": "Stock updated successfully", "new_stock": stock}

#####################
#   DELIVERIES
#####################

@manager_router.get("/deliveries")
async def view_deliveries(
    current_user_id: int = Depends(product_manager_required),
):
    query = load_sql_file("get_all_deliveries.sql")
    rows = await database.fetch_all(query)
    deliveries = [dict(row) for row in rows]
    return {"deliveries": deliveries}

@manager_router.patch("/deliveries/{delivery_id}/complete")
async def mark_delivery_completed(
    delivery_id: int,
    current_user_id: int = Depends(product_manager_required)
):
    # Check if the delivery exists
    check_query = "SELECT deliveryid FROM deliveries WHERE deliveryid = :did"
    row = await database.fetch_one(check_query, {"did": delivery_id})
    if not row:
        raise HTTPException(status_code=404, detail="Delivery not found")

    # Mark delivery as completed (no separate data class needed)
    update_query = """
        UPDATE deliveries
        SET completed = TRUE
        WHERE deliveryid = :did
    """
    await database.execute(update_query, {"did": delivery_id})

    return {"detail": "Delivery marked as completed"}

@manager_router.post("/deliveries/create", response_model=DeliveryRead)
async def create_delivery(
    delivery_data: DeliveryCreate,
    current_user_id: int = Depends(product_manager_required)
):
    """
    1) We find the first item from `order_items` for the given orderid.
    2) We insert a single row in `deliveries`.
    3) Return the newly created delivery.
    """

    # 1) SELECT from order_items + orders (limit to 1 item)
    fetch_item_query = """
        SELECT 
          o.userid AS customerid,
          oi.productid,
          oi.quantity,
          o.totalamount AS total_price
        FROM order_items oi
        JOIN orders o ON oi.orderid = o.orderid
        WHERE oi.orderid = :oid

    """
    item_row = await database.fetch_one(fetch_item_query, {"oid": delivery_data.orderid})
    if not item_row:
        raise HTTPException(status_code=404, detail="No items found for this order")

    # Extract needed fields
    customerid = item_row["customerid"]
    productid = item_row["productid"]
    quantity = item_row["quantity"]
    total_price = float(item_row["total_price"])  # convert if row is Decimal

    # 2) Insert a single row in deliveries
    insert_query = """
        INSERT INTO deliveries (
          orderid,
          customerid,
          productid,
          quantity,
          total_price,
          delivery_address,
          completed
        )
        VALUES (
          :orderid,
          :customerid,
          :productid,
          :quantity,
          :total_price,
          :delivery_address,
          FALSE
        )
        RETURNING 
          deliveryid,
          orderid,
          customerid,
          productid,
          quantity,
          total_price,
          delivery_address,
          completed
    """

    insert_values = {
        "orderid": delivery_data.orderid,
        "customerid": customerid,
        "productid": productid,
        "quantity": quantity,
        "total_price": total_price,
        "delivery_address": delivery_data.delivery_address,
    }

    new_row = await database.fetch_one(insert_query, insert_values)
    if not new_row:
        raise HTTPException(status_code=400, detail="Failed to create delivery")

    return DeliveryRead(**dict(new_row))




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

        