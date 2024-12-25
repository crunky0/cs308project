import sys

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # Assuming "main" includes the app with sales manager routes


client = TestClient(app)

# Test for setting product price
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_price(mock_execute):
    mock_execute.return_value = None  # Mock successful execution

    response = client.put("/set_price", json={"productid": 1, "new_price": 50.0})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Price updated successfully"}

# Test for setting product discount
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_discount(mock_execute):
    mock_execute.return_value = None  # Mock successful execution

    response = client.put("/set_discount", json={"productid": 1, "discount_price": 45.0})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Discount updated successfully"}

# Test for setting product cost
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_cost(mock_execute):
    mock_execute.return_value = None  # Mock successful execution

    response = client.put("/set_cost", json={"productid": 1, "new_cost": 30.0})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Cost updated successfully"}

# Test for generating profit/loss report
@patch("sales_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_profit_loss_report(mock_fetch_all):
    # Mock response from the database
    mock_fetch_all.return_value = [
        {"productid": 1, "profit_loss": 150.0},
        {"productid": 2, "profit_loss": -50.0},
    ]

    response = client.get("/profit_loss_report")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"productid": 1, "profit_loss": 150.0},
        {"productid": 2, "profit_loss": -50.0},
    ]

# Test for setting price with invalid data
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_price_invalid_data(mock_execute):
    response = client.put("/set_price", json={"productid": 1, "new_price": -10.0})

    # Assertions
    assert response.status_code == 422  # Validation error for negative price

# Test for setting discount with invalid data
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_discount_invalid_data(mock_execute):
    response = client.put("/set_discount", json={"productid": 1, "discount_price": -5.0})

    # Assertions
    assert response.status_code == 422  # Validation error for negative discount

# Test for setting cost with invalid data
@patch("sales_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_set_cost_invalid_data(mock_execute):
    response = client.put("/set_cost", json={"productid": 1, "new_cost": -20.0})

    # Assertions
    assert response.status_code == 422  # Validation error for negative cost
