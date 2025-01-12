# product_manager_endpoints.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List,Optional
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
#   PRODUCTS
#####################

@manager_router.post("/products")
async def add_product(
    productname: str,
    productmodel: str,
    description: str,
    distributerinfo: str,
    warranty: str,
    stock: int,
    categoryid: int,
    image: str
):
    """
    Add a new product with only the required fields. 
    Default values will be applied for price, cost, soldamount, discountPrice, and averageRating.
    """
    query = """
        INSERT INTO products (
            productName, productModel, description, distributerInfo, warranty, 
            stock, categoryID, image
        )
        VALUES (
            :productname, :productmodel, :description, :distributerinfo, :warranty,
            :stock, :categoryid, :image
        )
        RETURNING productID, productName, productModel, description, distributerInfo, 
                  warranty, stock, categoryID, image;
    """
    values = {
        "productname": productname,
        "productmodel": productmodel,
        "description": description,
        "distributerinfo": distributerinfo,
        "warranty": warranty,
        "stock": stock,
        "categoryid": categoryid,
        "image": image,
    }

    new_product = await database.fetch_one(query=query, values=values)

    if not new_product:
        raise HTTPException(status_code=400, detail="Failed to add product")

    return dict(new_product)


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
async def list_invoices(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    """
    Return a list of invoice filenames within the specified date range.
    """
    folder_path = "invoices"
    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="Invoices folder not found")

    # List all PDF files in the 'invoices' folder
    invoice_files = [
        file_name for file_name in os.listdir(folder_path)
        if file_name.lower().endswith(".pdf")
    ]

    # Parse and validate date parameters
    start_date_parsed = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date_parsed = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    print(f"Start date: {start_date_parsed}, End date: {end_date_parsed}")

    # Dynamically construct the SQL query
    query = "SELECT orderid, orderdate FROM orders WHERE 1=1"
    values = {}

    if start_date_parsed:
        query += " AND orderdate >= :start_date"
        values["start_date"] = start_date_parsed

    if end_date_parsed:
        query += " AND orderdate <= :end_date"
        values["end_date"] = end_date_parsed

    print(f"Final Query: {query}")
    print(f"Query Values: {values}")

    try:
        order_rows = await database.fetch_all(query=query, values=values)
    except Exception as e:
        print(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail="Database query failed.")

    # Extract valid order IDs
    valid_order_ids = {str(order["orderid"]) for order in order_rows}

    # Filter invoices based on valid file names
    filtered_invoices = []
    for file_name in invoice_files:
        try:
            # Validate the file name format
            order_id = file_name.split('-')[1].split('.')[0]
            if order_id in valid_order_ids:
                filtered_invoices.append(file_name)
        except IndexError:
            # Skip files that do not match the expected format
            print(f"Skipping invalid file: {file_name}")
            continue

    return filtered_invoices



@manager_router.get("/invoices/{filename}", response_class=FileResponse)
async def get_invoice(
    filename: str
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
        filename=filename,
        headers={"Content-Disposition": f"inline; filename={filename}"}
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

#####################
#   CATEGORIES
#####################
@manager_router.get("/categories", response_model=List[dict])
async def fetch_categories():
    """
    Fetch all categories.
    """
    query = "SELECT categoryid, name FROM categories ORDER BY categoryid ASC"
    categories = await database.fetch_all(query=query)
    return [{"categoryid": row["categoryid"], "name": row["name"]} for row in categories]

@manager_router.get("/products", response_model=List[dict])
async def fetch_products():
    """
    Fetch all products with their category names.
    """
    query = """
        SELECT 
            p.productid, 
            p.productname, 
            p.price, 
            p.stock, 
            c.name AS categoryname
        FROM 
            products p
        JOIN 
            categories c 
        ON 
            p.categoryid = c.categoryid
        ORDER BY 
            p.productid ASC
    """
    products = await database.fetch_all(query=query)
    return [
        {
            "productid": row["productid"],
            "productname": row["productname"],
            "price": row["price"],
            "stock": row["stock"],
            "categoryname": row["categoryname"],  # Now using the correct column name
        }
        for row in products
    ]
@manager_router.post("/categories")
async def add_category(name: str):
    """
    Add a new category.
    """
    query = "INSERT INTO categories (name) VALUES (:name) RETURNING categoryid, name"
    new_category = await database.fetch_one(query=query, values={"name": name})
    if not new_category:
        raise HTTPException(status_code=400, detail="Failed to create category")
    return {"categoryid": new_category["categoryid"], "name": new_category["name"]}

@manager_router.delete("/categories/{categoryid}")
async def delete_category(categoryid: int):
    """
    Delete a category and its associated products.
    """
    # Check if the category exists
    check_query = "SELECT categoryid FROM categories WHERE categoryid = :categoryid"
    category = await database.fetch_one(query=check_query, values={"categoryid": categoryid})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Delete all products in the category
    delete_products_query = "DELETE FROM products WHERE categoryid = :categoryid"
    await database.execute(query=delete_products_query, values={"categoryid": categoryid})

    # Delete the category
    delete_category_query = "DELETE FROM categories WHERE categoryid = :categoryid"
    await database.execute(query=delete_category_query, values={"categoryid": categoryid})

    return {"detail": f"Category {categoryid} and its associated products have been deleted"}


        