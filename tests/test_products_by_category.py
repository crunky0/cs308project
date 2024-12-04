import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

# Test for retrieving products by category ID
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_products_by_category(mock_fetch_all):
    # Mock product data for a category
    mock_fetch_all.return_value = [
        {
            "productid": 1,
            "serialnumber": 1001,
            "productname": "Product A",
            "productmodel": "Model A",
            "description": "Description for Product A",
            "distributerinfo": "Distributor Info A",
            "warranty": "1 Year",
            "price": 99.99,
            "stock": 10,
            "categoryid": 1,
            "soldamount": 5,
            "discountprice": None,
            "image": "http://example.com/image_a.jpg"
        },
        {
            "productid": 2,
            "serialnumber": 1002,
            "productname": "Product B",
            "productmodel": "Model B",
            "description": "Description for Product B",
            "distributerinfo": "Distributor Info B",
            "warranty": "2 Years",
            "price": 149.99,
            "stock": 20,
            "categoryid": 1,
            "soldamount": 8,
            "discountprice": 129.99,
            "image": "http://example.com/image_b.jpg"
        }
    ]

    response = client.get("/products/category/1/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {
            "productid": 1,
            "serialnumber": 1001,
            "productname": "Product A",
            "productmodel": "Model A",
            "description": "Description for Product A",
            "distributerinfo": "Distributor Info A",
            "warranty": "1 Year",
            "price": 99.99,
            "stock": 10,
            "categoryid": 1,
            "soldamount": 5,
            "discountprice": None,
            "image": "http://example.com/image_a.jpg"
        },
        {
            "productid": 2,
            "serialnumber": 1002,
            "productname": "Product B",
            "productmodel": "Model B",
            "description": "Description for Product B",
            "distributerinfo": "Distributor Info B",
            "warranty": "2 Years",
            "price": 149.99,
            "stock": 20,
            "categoryid": 1,
            "soldamount": 8,
            "discountprice": 129.99,
            "image": "http://example.com/image_b.jpg"
        }
    ]

# Test for category with no products
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_products_by_category_not_found(mock_fetch_all):
    # Mock no products for a category
    mock_fetch_all.return_value = []

    response = client.get("/products/category/999/")  # Category ID with no products

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "No products found for this category"}
