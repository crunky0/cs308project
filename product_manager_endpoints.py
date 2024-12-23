
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import product_manager_required
from db import database
from models import Product, Review, Invoice, Delivery
from schemas import (
    ProductCreate,
    ProductStockUpdate,
    ReviewUpdate,
    DeliveryStatusUpdate,
    InvoiceRead,
    DeliveryRead
)

manager_router = APIRouter(
    prefix="/product_manager_panel",
    tags=["product_manager_panel"]
)

# 1. Add a new product
@manager_router.post("/products", response_model=dict)
def add_product(
    product_data: ProductCreate,
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    product = Product(
        serialnumber=product_data.serialnumber,
        productname=product_data.productname,
        productmodel=product_data.productmodel,
        description=product_data.description,
        distributerinfo=product_data.distributerinfo,
        warranty=product_data.warranty,
        price=product_data.price,
        stock=product_data.stock,
        categoryid=product_data.categoryid
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"detail": "Product added successfully", "product_id": product.productid}

# 2. Remove a product
@manager_router.delete("/products/{product_id}", response_model=dict)
def remove_product(
    product_id: int,
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    product = db.query(Product).filter(Product.productid == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product removed successfully"}

# 3. Update product stock
@manager_router.patch("/products/{product_id}/stock", response_model=dict)
def update_product_stock(
    product_id: int,
    stock_data: ProductStockUpdate,
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    product = db.query(Product).filter(Product.productid == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if stock_data.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
    product.stock = stock_data.stock
    db.commit()
    db.refresh(product)
    return {
        "detail": "Stock updated successfully",
        "new_stock": product.stock
    }

# 4. Approve or reject reviews
@manager_router.patch("/reviews/{review_id}", response_model=dict)
def approve_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    review = db.query(Review).filter(Review.reviewid == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.approved = review_data.approved  # True or False
    db.commit()
    db.refresh(review)
    status_str = "approved" if review.approved else "rejected"
    return {"detail": f"Review {status_str} successfully"}

# 5. View all invoices
@manager_router.get("/invoices", response_model=list[InvoiceRead])
def get_invoices(
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    invoices = db.query(Invoice).all()
    return invoices

# (Optional) 6. View deliveries
@manager_router.get("/deliveries", response_model=list[DeliveryRead])
def get_deliveries(
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    """
    Only relevant if you have a Delivery table in your database.
    """
    deliveries = db.query(Delivery).all()
    return deliveries

# (Optional) 7. Update delivery status
@manager_router.patch("/deliveries/{delivery_id}", response_model=dict)
def update_delivery_status(
    delivery_id: int,
    delivery_update: DeliveryStatusUpdate,
    db: Session = Depends(database),
    current_user=Depends(product_manager_required)
):
    delivery = db.query(Delivery).filter(Delivery.deliveryid == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.status = delivery_update.status
    db.commit()
    db.refresh(delivery)
    return {
        "detail": "Delivery status updated successfully",
        "status": delivery.status
    }
