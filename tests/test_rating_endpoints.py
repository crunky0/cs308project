import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # or wherever your FastAPI app is defined

client = TestClient(app)


# ------------------------------------------------------------------------------
# 1) Test creating a review
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_create_review(mock_fetch_one):
    """
    The response model (ReviewResponse) apparently requires 'name' and 'surname'
    among others. We'll add them to the mocked DB row.
    """
    mock_fetch_one.return_value = {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": False,
        "name": "John",       # required by your model
        "surname": "Doe"      # required by your model
    }

    review_data = {
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!"
    }

    response = client.post("/reviews/", json=review_data)
    assert response.status_code == 200
    # We expect the entire model in the response
    assert response.json() == {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": False,
        "name": "John",
        "surname": "Doe"
    }


# ------------------------------------------------------------------------------
# 2) Test retrieving reviews for a product
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_reviews_for_product(mock_fetch_all):
    """
    Similarly, 'name' and 'surname' must exist for each row
    if your code always returns ReviewResponse.
    """
    mock_fetch_all.return_value = [
        {
            "reviewid": 1,
            "userid": 123,
            "productid": 456,
            "rating": 4.5,
            "comment": "Great product!",
            "approved": True,
            "name": "Alice",
            "surname": "Smith"
        },
        {
            "reviewid": 2,
            "userid": 124,
            "productid": 456,
            "rating": 3.0,
            "comment": "Average product.",
            "approved": True,
            "name": "Bob",
            "surname": "Johnson"
        }
    ]

    response = client.get("/products/456/reviews/")
    assert response.status_code == 200
    # The route returns List[ReviewResponse]
    assert response.json() == [
        {
            "reviewid": 1,
            "userid": 123,
            "productid": 456,
            "rating": 4.5,
            "comment": "Great product!",
            "approved": True,
            "name": "Alice",
            "surname": "Smith"
        },
        {
            "reviewid": 2,
            "userid": 124,
            "productid": 456,
            "rating": 3.0,
            "comment": "Average product.",
            "approved": True,
            "name": "Bob",
            "surname": "Johnson"
        }
    ]


# ------------------------------------------------------------------------------
# 3) Test approving a review
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review(mock_fetch_one):
    """
    The actual endpoint returns {"message": "Review approved successfully"}
    instead of returning the full review. So let's check that message.
    """
    # The DB row isn't actually returned in the final response, but we can mock it
    mock_fetch_one.return_value = {
        "reviewid": 1,
        "userid": 123,
        "productid": 456,
        "rating": 4.5,
        "comment": "Great product!",
        "approved": True
        # "name": "???" - not needed if the route doesn't include it in response
    }

    response = client.put("/reviews/1/approve/")
    assert response.status_code == 200
    # The route only returns this message, so let's check for that
    assert response.json() == {
        "message": "Review approved successfully"
    }


# ------------------------------------------------------------------------------
# 4) Test approving a non-existing review
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review_not_found(mock_fetch_one):
    # No matching record
    mock_fetch_one.return_value = None

    response = client.put("/reviews/999/approve/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found or already approved"}


# ------------------------------------------------------------------------------
# 5) Test average rating
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_average_rating(mock_fetch_one):
    mock_fetch_one.return_value = {"average_rating": 4.2}
    response = client.get("/products/456/average-rating/")
    assert response.status_code == 200
    assert response.json() == 4.2


# ------------------------------------------------------------------------------
# 6) Test average rating with no data
# ------------------------------------------------------------------------------
@patch("rating_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_average_rating_no_data(mock_fetch_one):
    # No ratings found => average_rating = None
    mock_fetch_one.return_value = {"average_rating": None}
    response = client.get("/products/999/average-rating/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No ratings found for this product"}
