import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app  # Adjust the import path to match your project structure

client = TestClient(app)


# Test: Add to wishlist
@patch("wishlist_endpoints.database.execute", new_callable=AsyncMock)
def test_add_to_wishlist(mock_execute):
    mock_execute.return_value = 1  # Simulate successful database insertion
    wishlist_item = {"userid": 1, "productid": 10}

    response = client.post("/wishlist/add", json=wishlist_item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to wishlist"}
    mock_execute.assert_called_once_with(
        query="SQL FROM FILE CONTENT HERE",  # Replace with the actual SQL query content
        values={"userid": wishlist_item["userid"], "productid": wishlist_item["productid"]}
    )


@patch("wishlist_endpoints.database.execute", new_callable=AsyncMock)
def test_add_to_wishlist_error(mock_execute):
    mock_execute.side_effect = Exception("Database error")
    wishlist_item = {"userid": 1, "productid": 10}

    response = client.post("/wishlist/add", json=wishlist_item)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error adding to wishlist: Database error"}


# Test: Remove from wishlist
@patch("wishlist_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_from_wishlist(mock_execute):
    mock_execute.return_value = 1  # Simulate successful deletion
    wishlist_item = {"userid": 1, "productid": 10}

    response = client.delete("/wishlist/remove", json=wishlist_item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item removed from wishlist"}


@patch("wishlist_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_from_wishlist_not_found(mock_execute):
    mock_execute.return_value = 0  # Simulate no rows affected
    wishlist_item = {"userid": 1, "productid": 10}

    response = client.delete("/wishlist/remove", json=wishlist_item)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found in wishlist"}


@patch("wishlist_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_from_wishlist_error(mock_execute):
    mock_execute.side_effect = Exception("Database error")
    wishlist_item = {"userid": 1, "productid": 10}

    response = client.delete("/wishlist/remove", json=wishlist_item)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error removing from wishlist: Database error"}


# Test: Fetch wishlist
@patch("wishlist_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_wishlist(mock_fetch_all):
    mock_fetch_all.return_value = [
        {"productid": 10, "productname": "Product A"},
        {"productid": 20, "productname": "Product B"},
    ]
    userid = 1

    response = client.get(f"/wishlist/{userid}")
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 10, "productname": "Product A"},
        {"productid": 20, "productname": "Product B"},
    ]


@patch("wishlist_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_wishlist_empty(mock_fetch_all):
    mock_fetch_all.return_value = []
    userid = 1

    response = client.get(f"/wishlist/{userid}")
    assert response.status_code == 200
    assert response.json() == []


@patch("wishlist_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_wishlist_error(mock_fetch_all):
    mock_fetch_all.side_effect = Exception("Database error")
    userid = 1

    response = client.get(f"/wishlist/{userid}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Error fetching wishlist: Database error"}
