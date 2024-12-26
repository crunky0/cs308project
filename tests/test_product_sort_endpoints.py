import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

# Test for sorting products by price in ascending order
@patch("product_sort_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_price_asc(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
    ]

    response = client.get("/products/sort/price/asc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
    ]

# Test for sorting products by price in descending order
@patch("product_sort_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_price_desc(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
    ]

    response = client.get("/products/sort/price/desc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
    ]

# Test for sorting products by popularity in ascending order
@patch("product_sort_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_popularity_asc(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
    ]

    response = client.get("/products/sort/popularity/asc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
    ]

# Test for sorting products by popularity in descending order
@patch("product_sort_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_sort_products_by_popularity_desc(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
    ]

    response = client.get("/products/sort/popularity/desc/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 1, "productname": "Product A", "price": 10.0, "soldamount": 50},
        {"productid": 2, "productname": "Product B", "price": 20.0, "soldamount": 30},
    ]
