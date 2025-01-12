import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # Adjust this import to point to your FastAPI app

client = TestClient(app)

# 1) Test: Fetch stock for an existing product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_stock_existing_product(mock_fetch_one):
    # Mock DB response
    mock_fetch_one.return_value = {
        "productid": 1,
        "serialnumber": 12345,
        "productname": "Sample Product",
        "productmodel": "SP-01",
        "description": "A sample product",
        "distributerinfo": "Sample Distributor",
        "warranty": "1 year",
        "price": 100.0,
        "stock": 50,
        "categoryid": 2,
    }

    response = client.get("/products/1")  # Call the endpoint
    assert response.status_code == 200
    assert response.json() == "50 items available."

# 2) Test: Fetch stock for a product that is out of stock
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_stock_out_of_stock_product(mock_fetch_one):
    # Mock DB response
    mock_fetch_one.return_value = {
        "productid": 2,
        "serialnumber": 12346,
        "productname": "Out of Stock Product",
        "productmodel": "OSP-01",
        "description": "An out-of-stock product",
        "distributerinfo": "Sample Distributor",
        "warranty": "1 year",
        "price": 150.0,
        "stock": 0,
        "categoryid": 3,
    }

    response = client.get("/products/2")  # Call the endpoint
    assert response.status_code == 200
    assert response.json() == "Out of Stock."

# 3) Test: Fetch stock for a non-existent product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_stock_nonexistent_product(mock_fetch_one):
    # Mock DB response as None
    mock_fetch_one.return_value = None

    response = client.get("/products/9999")  # Call the endpoint for a non-existent product
    assert response.status_code == 400
    assert response.json() == {"detail": "Selected product cannot be found."}

# 4) Test: Database error during stock fetch
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_stock_database_error(mock_fetch_one):
    # Simulate a database exception
    mock_fetch_one.side_effect = Exception("Database error")

    response = client.get("/products/1")  # Call the endpoint
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
