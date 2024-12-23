# product_manager_endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from databases import Database
from typing import List

from db import database
from dependencies import get_database, product_manager_required
from schemas import (
    CategoryCreate,
    ProductCreate,
    ProductStockUpdate,
    ReviewApproval,
    DeliveryUpdate,
    InvoiceRead
)

manager_router = APIRouter(
    prefix="/productmanagerpanel",
    tags=["product_manager_panel"]
)

#####################
#   CATEGORY
#####################

@manager_router.post("/categories")
async def add_category(
    category_data: CategoryCreate,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database),
):
    query = """
        INSERT INTO categories (name)
        VALUES (:name)
        RETURNING categoryid
    """
    values = {"name": category_data.name}
    categoryid = await db.fetch_val(query, values)
    return {"detail": "Category added successfully", "categoryid": categoryid}

@manager_router.delete("/categories/{category_id}")
async def remove_category(
    category_id: int,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database),
):
    # check if exists
    check_query = "SELECT categoryid FROM categories WHERE categoryid = :cat_id"
    row = await db.fetch_one(check_query, {"cat_id": category_id})
    if not row:
        raise HTTPException(status_code=404, detail="Category not found")

    delete_query = "DELETE FROM categories WHERE categoryid = :cat_id"
    await db.execute(delete_query, {"cat_id": category_id})
    return {"detail": "Category removed successfully"}

#####################
#   PRODUCTS
#####################

@manager_router.post("/products")
async def add_product(
    product_data: ProductCreate,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
):
    query = """
        INSERT INTO products (
            categoryid, productname, productmodel, description,
            distributerinfo, warranty, price, stock
        ) 
        VALUES (
            :categoryid, :productname, :productmodel, :description,
            :distributerinfo, :warranty, :price, :stock
        )
        RETURNING productid
    """
    values = product_data.dict()
    productid = await db.fetch_val(query, values)
    return {"detail": "Product added successfully", "product_id": productid}

@manager_router.delete("/products/{product_id}")
async def remove_product(
    product_id: int,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
):
    check_query = "SELECT productid FROM products WHERE productid = :pid"
    row = await db.fetch_one(check_query, {"pid": product_id})
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_query = "DELETE FROM products WHERE productid = :pid"
    await db.execute(delete_query, {"pid": product_id})
    return {"detail": "Product removed successfully"}

@manager_router.patch("/products/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    stock_data: ProductStockUpdate,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
):
    # check product
    check_query = "SELECT stock FROM products WHERE productid = :pid"
    product_row = await db.fetch_one(check_query, {"pid": product_id})
    if not product_row:
        raise HTTPException(status_code=404, detail="Product not found")

    if stock_data.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    update_query = """
        UPDATE products
        SET stock = :stock
        WHERE productid = :pid
    """
    await db.execute(update_query, {"stock": stock_data.stock, "pid": product_id})
    return {"detail": "Stock updated successfully", "new_stock": stock_data.stock}

#####################
#   DELIVERIES
#####################

@manager_router.get("/deliveries")
async def view_deliveries(
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
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
    delivery_update: DeliveryUpdate,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
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
    db: Database = Depends(get_database)
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
    rows = await db.fetch_all(query)
    return [InvoiceRead(**dict(row)) for row in rows]

#####################
#   REVIEWS
#####################

@manager_router.patch("/reviews/{review_id}")
async def approve_or_disapprove_review(
    review_id: int,
    data: ReviewApproval,
    current_user_id: int = Depends(product_manager_required),
    db: Database = Depends(get_database)
):
    check_query = "SELECT reviewid FROM reviews WHERE reviewid = :rid"
    row = await db.fetch_one(check_query, {"rid": review_id})
    if not row:
        raise HTTPException(status_code=404, detail="Review not found")

    update_query = """
        UPDATE reviews
        SET approved = :approved
        WHERE reviewid = :rid
    """
    await db.execute(update_query, {"approved": data.approved, "rid": review_id})
    status_str = "approved" if data.approved else "disapproved"
    return {"detail": f"Review {status_str} successfully"}
