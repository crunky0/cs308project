from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from db import database
import os
from typing import List

router = APIRouter()

# Helper function to load SQL files
def load_sql_file(filename: str) -> str:
    file_path = os.path.join("sql", filename)
    with open(file_path, "r") as file:
        return file.read()

class ReviewCreate(BaseModel):
    userid: int
    productid: int
    rating: float
    comment: str

class ReviewResponse(BaseModel):
    reviewid: int
    userid: int
    productid: int
    rating: float
    comment: Optional[str] 
    approved: bool
    name: Optional[str]  # User's name
    surname: Optional[str]

@router.post("/reviews/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate):
    # Load the SQL query from the file
    create_review_query = load_sql_file("create_review.sql")
    
    values = {
        "userid": review.userid,
        "productid": review.productid,
        "rating": review.rating,
        "comment": review.comment,
        "approved": False  # By default, the review is not approved
    }
    
    review_record = await database.fetch_one(query=create_review_query, values=values)
    if not review_record:
        raise HTTPException(status_code=400, detail="Failed to create review")
    
    return ReviewResponse(**review_record)

# Endpoint to retrieve all reviews for a specific product
@router.get("/products/{productid}/reviews/", response_model=List[ReviewResponse])
async def get_reviews_for_product(productid: int):
    query = load_sql_file("get_reviews_for_product.sql")  # Updated SQL file
    reviews = await database.fetch_all(query=query, values={"productid": productid})
    return [ReviewResponse(**review) for review in reviews]




@router.put("/reviews/{reviewid}/approve/")
async def approve_review(reviewid: int):
    # Load the SQL query from the file
    approve_review_query = load_sql_file("approve_rating.sql")

    # Execute the query to approve the rating
    review_record = await database.fetch_one(query=approve_review_query, values={"reviewid": reviewid})
    if not review_record:
        raise HTTPException(status_code=404, detail="Review not found or already approved")
    
    # Return a success response
    return JSONResponse(content={"message": "Review approved successfully"}, status_code=200)


@router.get("/products/{productid}/average-rating/", response_model=float)
async def get_average_rating(productid: int):
    """
    Get the average rating for a specific product.
    """
    # Load the SQL query from the file
    average_rating_query = load_sql_file("average_rating.sql")
    
    # Execute the query to calculate the average rating
    result = await database.fetch_one(query=average_rating_query, values={"productid": productid})
    
    if not result or result["average_rating"] is None:
        raise HTTPException(status_code=404, detail="No ratings found for this product")
    
    return result["average_rating"]

@router.get("/reviews/not-approved/", response_model=List[ReviewResponse])
async def get_not_approved_reviews():
    """
    Fetch all reviews that are not approved.
    """
    # Load the SQL query from the file
    not_approved_reviews_query = load_sql_file("get_not_approved_reviews.sql")

    # Execute the query to fetch all not-approved reviews
    reviews = await database.fetch_all(query=not_approved_reviews_query)

    return [ReviewResponse(**review) for review in reviews]

@router.delete("/reviews/{reviewid}/", status_code=204)
async def delete_review(reviewid: int):
    """
    Delete a review by its ID.
    """
    # Load the SQL query from the file
    delete_review_query = load_sql_file("delete_review.sql")
    
    # Execute the query to delete the review
    result = await database.execute(query=delete_review_query, values={"reviewid": reviewid})
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"detail": "Review deleted successfully"}
