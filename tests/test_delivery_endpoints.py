# tests/test_delivery_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from datetime import datetime

# Adjust import to match where your FastAPI `app` is actually defined
from main import app  

# If your code is literally in a file named `delivery_endpoints.py`
# with the statement: `from db import database` and `from dependencies import product_manager_required`,
# then these patch targets should work as shown below.

client = TestClient(app)


@pytest.fixture
def dummy_manager_user():
    """
    You might have a Pydantic 'User' model that includes fields like 'id', 'role', etc.
    Here we'll just return a simple object or dict that your `product_manager_required` might produce.
    """
    # For instance:
    class User:
        id: int = 42
        role: str = "Productmanager"
    return User()


###############################################################################
#  GET /deliveries/{deliveryid}
###############################################################################

@patch("delivery_endpoints.product_manager_required")
@patch("delivery_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_delivery_success(mock_fetch_one, mock_pm_required, dummy_manager_user):
    """
    Test a successful GET /deliveries/{deliveryid} where the delivery is found.
    """
    # Mock the 'product_manager_required' dependency so it returns a user object
    mock_pm_required.return_value = dummy_manager_user

    # Mock DB to return a matching row
    mock_fetch_one.return_value = {
        "deliveryid": 123,
        "orderid": 10,
        "status": "processing",
        "created_at": datetime(2023, 1, 1, 12, 0, 0),  # or any datetime
    }

    response = client.get("/deliveries/123")
    assert response.status_code == 200
    assert response.json() == {
        "deliveryid": 123,
        "orderid": 10,
        "status": "processing",
        "created_at": "2023-01-01T12:00:00",  # ISO format
    }


@patch("delivery_endpoints.product_manager_required")
@patch("delivery_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_delivery_not_found(mock_fetch_one, mock_pm_required, dummy_manager_user):
    """
    Test GET /deliveries/{deliveryid} when the delivery does not exist -> 404
    """
    mock_pm_required.return_value = dummy_manager_user
    mock_fetch_one.return_value = None  # not found

    response = client.get("/deliveries/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Delivery not found"}


###############################################################################
#  DELETE /deliveries/{deliveryid}/delete
###############################################################################

@patch("delivery_endpoints.product_manager_required")
@patch("delivery_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("delivery_endpoints.database.execute", new_callable=AsyncMock)
def test_delete_delivery_success(mock_execute, mock_fetch_one, mock_pm_required, dummy_manager_user):
    """
    Test DELETE /deliveries/{deliveryid}/delete when the delivery is found -> 200
    """
    mock_pm_required.return_value = dummy_manager_user

    # Mock that the delivery exists
    mock_fetch_one.return_value = {"deliveryid": 123}

    response = client.delete("/deliveries/123/delete")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delivery deleted successfully"}

    # Optionally, ensure the correct DELETE query was triggered
    # e.g. mock_execute.assert_awaited_once_with( ... ) if you want to check specifics


@patch("delivery_endpoints.product_manager_required")
@patch("delivery_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_delete_delivery_not_found(mock_fetch_one, mock_pm_required, dummy_manager_user):
    """
    Test DELETE /deliveries/{deliveryid}/delete when the delivery doesn't exist -> 404
    """
    mock_pm_required.return_value = dummy_manager_user
    mock_fetch_one.return_value = None  # Delivery not found

    response = client.delete("/deliveries/9999/delete")
    assert response.status_code == 404
    assert response.json() == {"detail": "Delivery not found"}
