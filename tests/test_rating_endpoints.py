import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
from rating_endpoints import ReviewCreate, ReviewResponse  

client = TestClient(app)

# Test for creating a review
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_create_review(mock_fetch_one):
    # Mock response from the database
    mock_fetch_one.return_value = {
        "reviewID": 1,
        "userID": 123,
        "productID": 456,
        "review": 4.5,
        "comment": "Great product!",
        "approved": False
    }

    # Mock input data
    review_data = {
        "userID": 123,
        "productID": 456,
        "review": 4.5,
        "comment": "Great product!"
    }

    response = client.post("/reviews/", json=review_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "reviewID": 1,
        "userID": 123,
        "productID": 456,
        "review": 4.5,
        "comment": "Great product!",
        "approved": False
    }

# Test for retrieving reviews for a product
@patch("rating_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_reviews_for_product(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {
            "reviewID": 1,
            "userID": 123,
            "productID": 456,
            "review": 4.5,
            "comment": "Great product!",
            "approved": True
        },
        {
            "reviewID": 2,
            "userID": 124,
            "productID": 456,
            "review": 3.0,
            "comment": "Average product.",
            "approved": True
        }
    ]

    response = client.get("/products/456/reviews/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {
            "reviewID": 1,
            "userID": 123,
            "productID": 456,
            "review": 4.5,
            "comment": "Great product!",
            "approved": True
        },
        {
            "reviewID": 2,
            "userID": 124,
            "productID": 456,
            "review": 3.0,
            "comment": "Average product.",
            "approved": True
        }
    ]

# Test for approving a review
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review(mock_fetch_one):
    # Mock response from the database
    mock_fetch_one.return_value = {
        "reviewID": 1,
        "userID": 123,
        "productID": 456,
        "review": 4.5,
        "comment": "Great product!",
        "approved": True
    }

    response = client.put("/reviews/1/approve/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "reviewID": 1,
        "userID": 123,
        "productID": 456,
        "review": 4.5,
        "comment": "Great product!",
        "approved": True
    }

# Test for approving a non-existing review
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review_not_found(mock_fetch_one):
    # Mock response from the database (no matching record)
    mock_fetch_one.return_value = None

    response = client.put("/reviews/999/approve/")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found or already approved"}

