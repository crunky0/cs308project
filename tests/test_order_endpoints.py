import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app  # Assuming the app is created in `main.py`
from order_service import OrderService  # Path to your order service

client = TestClient(app)

# Mock order data
order_data = {
    "userid": 1,
    "totalamount": 200.0,
    "items": [
        {"productid": 1, "quantity": 2, "price": 50.0},
        {"productid": 2, "quantity": 1, "price": 100.0},
    ],
}


# Test for successful order creation
@patch("order_service.OrderService.create_order", new_callable=AsyncMock)
def test_create_order_success(mock_create_order):
    # Mock response from the service
    mock_create_order.return_value = {"orderid": 123, "message": "Order created successfully"}

    response = client.post("/create_order/", json=order_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"orderid": 123, "message": "Order created successfully"}


# Test for order creation with insufficient stock
@patch("order_service.OrderService.create_order", new_callable=AsyncMock)
def test_create_order_insufficient_stock(mock_create_order):
    # Mock insufficient stock exception
    mock_create_order.side_effect = ValueError("Insufficient stock for product ID 1")

    response = client.post("/create_order/", json=order_data)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient stock for product ID 1"}


# Test for database error during order creation
@patch("order_service.OrderService.create_order", new_callable=AsyncMock)
def test_create_order_database_error(mock_create_order):
    # Mock database error
    mock_create_order.side_effect = Exception("Database error: Database query failed")

    response = client.post("/create_order/", json=order_data)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error: Database query failed"}
