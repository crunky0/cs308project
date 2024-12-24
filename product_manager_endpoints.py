# product_manager_endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from dependencies import  product_manager_required

from product_endpoints import ProductCreate
from db import database


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
    row = await database.fetch_one(query, {"pid": product_id})
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_query = load_sql_file("remove_product.sql")
    await database.execute(delete_query, {"pid": product_id})
    return {"detail": "Product removed successfully"}

@manager_router.patch("/products/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    stock: int,
    current_user_id: int = Depends(product_manager_required),
 
):
    # check product
    query = load_sql_file("find_product.sql")
    product_row = await database.fetch_one(query, {"pid": product_id})
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
    query = """
        SELECT
            deliveryid,
            userid AS customer_id,
            productid,
            quantity,
            total_price,
            delivery_address,
            completed
        FROM deliveries
    """
    rows = await db.fetch_all(query)
    deliveries = [dict(row) for row in rows]
    return {"deliveries": deliveries}

@manager_router.patch("/deliveries/{delivery_id}/complete")
async def mark_delivery_completed(
    delivery_id: int,
    current_user_id: int = Depends(product_manager_required),

):
    check_query = "SELECT deliveryid FROM deliveries WHERE deliveryid = :did"
    row = await db.fetch_one(check_query, {"did": delivery_id})
    if not row:
        raise HTTPException(status_code=404, detail="Delivery not found")

    update_query = "UPDATE deliveries SET completed = :completed WHERE deliveryid = :did"
    await db.execute(update_query, {"completed": delivery_update.completed, "did": delivery_id})
    status_str = "completed" if delivery_update.completed else "not completed"
    return {"detail": f"Delivery marked as {status_str}"}

#####################
#   INVOICES
#####################

@manager_router.get("/invoices", response_model=List[InvoiceRead])
async def get_invoices(
    current_user_id: int = Depends(product_manager_required),
):
    query = """
        SELECT 
            invoiceid,
            orderid,
            invoice_number,
            invoice_date,
            file_path
        FROM invoices
        ORDER BY invoiceid
    """
    rows = await database.fetch_all(query)
    return [InvoiceRead(**dict(row)) for row in rows]

#####################
#   REVIEWS
#####################

@manager_router.patch("/reviews/{review_id}")
async def approve_or_disapprove_review(
    review_id: int,
    current_user_id: int = Depends(product_manager_required),
):
    check_query = "SELECT reviewid FROM reviews WHERE reviewid = :rid"
    row = await database.fetch_one(check_query, {"rid": review_id})
    if not row:
        raise HTTPException(status_code=404, detail="Review not found")

    update_query = """
        UPDATE reviews
        SET approved = :approved
        WHERE reviewid = :rid
    """
    await database.execute(update_query, {"approved": data.approved, "rid": review_id})
    status_str = "approved" if data.approved else "disapproved"
    return {"detail": f"Review {status_str} successfully"}
        