import sys
sys.path.append(".")
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

# Test for getting a product by ID
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_product_by_id(mock_fetch_one):
    # Mock database response
    mock_fetch_one.return_value = {
        "productID": 1,
        "productName": "Laptop",
        "productModel": "XYZ123",
        "description": "High-performance laptop",
        "price": 1200.00,
        "stock": 10,
        "categoryID": 1,
    }

    response = client.get("/products/1/")
    
    assert response.status_code == 200
    assert response.json() == {
        "productID": 1,
        "productName": "Laptop",
        "productModel": "XYZ123",
        "description": "High-performance laptop",
        "price": 1200.00,
        "stock": 10,
        "categoryID": 1,
    }

# Test for searching products by name
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_search_products_by_name(mock_fetch_all):
    mock_fetch_all.return_value = [
        {"productID": 1, "productName": "Laptop", "price": 1200.00},
        {"productID": 2, "productName": "Laptop Sleeve", "price": 20.00},
    ]

    response = client.get("/products/search/name/?productName=Laptop")

    assert response.status_code == 200
    assert response.json() == [
        {"productID": 1, "productName": "Laptop", "price": 1200.00},
        {"productID": 2, "productName": "Laptop Sleeve", "price": 20.00},
    ]

# Test for adding a product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_product(mock_fetch_one):
    # Mock database response for the added product
    mock_fetch_one.return_value = {
        "productID": 3,
        "productName": "Mouse",
        "price": 25.00,
        "stock": 100,
    }

    product_data = {
        "serialnumber": 12345,
        "productname": "Mouse",
        "productmodel": "ABC123",
        "description": "Wireless mouse",
        "distributerinfo": "Tech Supplies",
        "warranty": "1 year",
        "price": 25.00,
        "stock": 100,
        "categoryid": 2,
        "soldamount": 0,
        "discountprice": None,
        "image": "mouse.jpg",
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 200
    assert response.json() == {
        "productID": 3,
        "productName": "Mouse",
        "price": 25.00,
        "stock": 100,
    }

# Test for removing a product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_product(mock_fetch_one):
    mock_fetch_one.return_value = {
        "productID": 3,
        "productName": "Mouse",
        "price": 25.00,
        "stock": 100,
    }

    response = client.delete("/products/3/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Product removed successfully",
        "product": {
            "productID": 3,
            "productName": "Mouse",
            "price": 25.00,
            "stock": 100,
        },
    }

# Test for adding a discount to a product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_discount(mock_fetch_one):
    # Mock response for a successful discount addition
    mock_fetch_one.return_value = {
        "productID": 1,
        "productName": "Laptop",
        "price": 1200.00,
        "discountPrice": 1000.00,
    }

    # Request body for adding the discount
    request_body = {"discountPrice": 1000.00}

    # Send PUT request
    response = client.put("/products/1/discount/", json=request_body)

    # Assertions for success scenario
    assert response.status_code == 200
    assert response.json() == {
        "message": "Discount added successfully",
        "product": {
            "productID": 1,
            "productName": "Laptop",
            "price": 1200.00,
            "discountPrice": 1000.00,
        },
    }

# Test for removing a discount from a product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_discount(mock_fetch_one):
    mock_fetch_one.return_value = {
        "productID": 1,
        "productName": "Laptop",
        "price": 1200.00,
        "discountPrice": None,
    }

    response = client.put("/products/1/discount/remove/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Discount removed successfully",
        "product": {
            "productID": 1,
            "productName": "Laptop",
            "price": 1200.00,
            "discountPrice": None,
        },
    }
