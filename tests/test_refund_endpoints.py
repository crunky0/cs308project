import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app  # Adjust the import path to match your project's structure

client = TestClient(app)

# Test: Validate refund eligibility
@patch("refund_endpoints.RefundService.validate_order_for_refund", new_callable=AsyncMock)
def test_validate_refund_valid(mock_validate_order_for_refund):
    mock_validate_order_for_refund.return_value = None  # No exception means valid
    response = client.get("/refund/validate/1")
    assert response.status_code == 200
    assert response.json() == {"orderid": 1, "valid": True}

@patch("refund_endpoints.RefundService.validate_order_for_refund", new_callable=AsyncMock)
def test_validate_refund_invalid(mock_validate_order_for_refund):
    mock_validate_order_for_refund.side_effect = ValueError("Refund period expired")
    response = client.get("/refund/validate/1")
    assert response.status_code == 200
    assert response.json() == {"orderid": 1, "valid": False, "reason": "Refund period expired"}

# Test: Get refundable products
@patch("refund_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_refundable_products(mock_fetch_all):
    mock_fetch_all.return_value = [{"productid": 101, "quantity": 2}, {"productid": 102, "quantity": 1}]
    response = client.get("/refund/select/1")
    assert response.status_code == 200
    assert response.json() == {
        "orderid": 1,
        "products": [{"productid": 101, "quantity": 2}, {"productid": 102, "quantity": 1}]
    }

@patch("refund_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_refundable_products_empty(mock_fetch_all):
    mock_fetch_all.return_value = []
    response = client.get("/refund/select/1")
    assert response.status_code == 200
    assert response.json() == {"orderid": 1, "products": []}

# Test: Submit refund request
@patch("refund_endpoints.database.transaction", new_callable=AsyncMock)
@patch("refund_endpoints.database.execute", new_callable=AsyncMock)
def test_request_refund(mock_execute, mock_transaction):
    refund_request_data = {
        "orderid": 1,
        "products": [{"productid": 101, "quantity": 1}, {"productid": 102, "quantity": 2}]
    }
    response = client.post("/refund/request", json=refund_request_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Refund request submitted and pending manager approval."}
    assert mock_execute.call_count == len(refund_request_data["products"])

# Test: Manager decision - Approve
@patch("refund_endpoints.database.fetch_all", new_callable=AsyncMock)
@patch("refund_endpoints.database.execute", new_callable=AsyncMock)
@patch("refund_endpoints.RefundService.process_refund", new_callable=AsyncMock)
def test_manager_decision_approve(mock_process_refund, mock_execute, mock_fetch_all):
    mock_fetch_all.return_value = [{"productid": 101, "quantity": 1}, {"productid": 102, "quantity": 2}]
    mock_process_refund.return_value = 150.0
    mock_execute.return_value = None

    decision_data = {"orderid": 1, "approved": True}
    response = client.post("/refund/decision", json=decision_data)

    assert response.status_code == 200
    assert response.json() == {"orderid": 1, "refunded_amount": 150.0, "status": "Refunded"}
    mock_process_refund.assert_called_once()

# Test: Manager decision - Deny
@patch("refund_endpoints.database.execute", new_callable=AsyncMock)
def test_manager_decision_deny(mock_execute):
    mock_execute.return_value = None
    decision_data = {"orderid": 1, "approved": False}
    response = client.post("/refund/decision", json=decision_data)
    assert response.status_code == 200
    assert response.json() == {"orderid": 1, "refunded_amount": 0.0, "status": "Denied"}

# Test: Fetch all refund requests
@patch("refund_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_all_refund_requests(mock_fetch_all):
    mock_fetch_all.return_value = [{"orderid": 1, "productid": 101, "quantity": 1}]
    response = client.get("/refund/requests")
    assert response.status_code == 200
    assert response.json() == [{"orderid": 1, "productid": 101, "quantity": 1}]

@patch("refund_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_all_refund_requests_empty(mock_fetch_all):
    mock_fetch_all.return_value = []
    response = client.get("/refund/requests")
    assert response.status_code == 200
    assert response.json() == []
