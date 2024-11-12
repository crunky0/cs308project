from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from db import database
import os

router = APIRouter()

# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()

class ReviewCreate(BaseModel):
    userID: int
    productID: int
    review: float
    comment: str

class ReviewResponse(BaseModel):
    reviewID: int
    userID: int
    productID: int
    review: float
    comment: str
    approved: bool

@router.post("/reviews/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate):
    # Load the SQL query from the file
    create_review_query = load_sql_file("create_review.sql")
    
    values = {
        "userID": review.userID,
        "productID": review.productID,
        "review": review.review,
        "comment": review.comment,
        "approved": False  # By default, the review is not approved
    }
    
    review_record = await database.fetch_one(query=create_review_query, values=values)
    if not review_record:
        raise HTTPException(status_code=400, detail="Failed to create review")
    
    return ReviewResponse(**review_record)

# Endpoint to retrieve all reviews for a specific product
@router.get("/products/{product_id}/reviews/", response_model=list[ReviewResponse])
async def get_reviews_for_product(product_id: int):
    # Load the SQL query from the file
    get_reviews_query = load_sql_file("get_reviews_for_product.sql")
    
    reviews = await database.fetch_all(query=get_reviews_query, values={"productID": product_id})
    return [ReviewResponse(**review) for review in reviews]
