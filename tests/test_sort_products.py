import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # Replace with the actual file where your app is defined

client = TestClient(app)

# Test for products sorted by price in ascending order
@patch("products_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_price_asc(mock_fetch_all):
    # Mock sorted products by price (ascending)
    mock_fetch_all.return_value = [
        {"productid": 1, "price": 10.0, "productname": "Product A"},
        {"productid": 2, "price": 20.0, "productname": "Product B"},
        {"productid": 3, "price": 30.0, "productname": "Product C"},
    ]

    response = client.get("/products/sort/price/asc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 1, "price": 10.0, "productname": "Product A"},
        {"productid": 2, "price": 20.0, "productname": "Product B"},
        {"productid": 3, "price": 30.0, "productname": "Product C"},
    ]

# Test for products sorted by price in descending order
@patch("products_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_price_desc(mock_fetch_all):
    # Mock sorted products by price (descending)
    mock_fetch_all.return_value = [
        {"productid": 3, "price": 30.0, "productname": "Product C"},
        {"productid": 2, "price": 20.0, "productname": "Product B"},
        {"productid": 1, "price": 10.0, "productname": "Product A"},
    ]

    response = client.get("/products/sort/price/desc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 3, "price": 30.0, "productname": "Product C"},
        {"productid": 2, "price": 20.0, "productname": "Product B"},
        {"productid": 1, "price": 10.0, "productname": "Product A"},
    ]

# Test for products sorted by popularity (soldAmount) in ascending order
@patch("products_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_popularity_asc(mock_fetch_all):
    # Mock sorted products by popularity (ascending)
    mock_fetch_all.return_value = [
        {"productid": 1, "soldamount": 5, "productname": "Product A"},
        {"productid": 2, "soldamount": 10, "productname": "Product B"},
        {"productid": 3, "soldamount": 15, "productname": "Product C"},
    ]

    response = client.get("/products/sort/popularity/asc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 1, "soldamount": 5, "productname": "Product A"},
        {"productid": 2, "soldamount": 10, "productname": "Product B"},
        {"productid": 3, "soldamount": 15, "productname": "Product C"},
    ]

# Test for products sorted by popularity (soldAmount) in descending order
@patch("products_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_popularity_desc(mock_fetch_all):
    # Mock sorted products by popularity (descending)
    mock_fetch_all.return_value = [
        {"productid": 3, "soldamount": 15, "productname": "Product C"},
        {"productid": 2, "soldamount": 10, "productname": "Product B"},
        {"productid": 1, "soldamount": 5, "productname": "Product A"},
    ]

    response = client.get("/products/sort/popularity/desc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 3, "soldamount": 15, "productname": "Product C"},
        {"productid": 2, "soldamount": 10, "productname": "Product B"},
        {"productid": 1, "soldamount": 5, "productname": "Product A"},
    ]
