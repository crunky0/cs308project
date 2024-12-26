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
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": False
    }

    # Mock input data
    review_data = {
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!"
    }

    response = client.post("/reviews/", json=review_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": False
    }

# Test for retrieving reviews for a product
@patch("rating_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_reviews_for_product(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {
            "reviewid": 1,
            "userid": 123,
            "productid": 456,
            "rating": 4.5,
            "comment": "Great product!",
            "approved": True
        },
        {
            "reviewid": 2,
            "userid": 124,
            "productid": 456,
            "rating": 3.0,
            "comment": "Average product.",
            "approved": True
        }
    ]

    response = client.get("/products/456/reviews/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {
            "reviewid": 1,
            "userid": 123,
            "productid": 456,
            "rating": 4.5,
            "comment": "Great product!",
            "approved": True
        },
        {
            "reviewid": 2,
            "userid": 124,
            "productid": 456,
            "rating": 3.0,
            "comment": "Average product.",
            "approved": True
        }
    ]

# Test for approving a review
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review(mock_fetch_one):
    # Mock response from the database
    mock_fetch_one.return_value = {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": True
    }

    response = client.put("/reviews/1/approve/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
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

# Test for average rating
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_average_rating(mock_fetch_one):
    # Mock response from the database
    mock_fetch_one.return_value = {"average_rating": 4.2}

    response = client.get("/products/456/average-rating/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == 4.2

# Test for average rating with no data
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_average_rating_no_data(mock_fetch_one):
    # Mock response from the database (no ratings found)
    mock_fetch_one.return_value = {"average_rating": None}

    response = client.get("/products/999/average-rating/")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "No ratings found for this product"}
