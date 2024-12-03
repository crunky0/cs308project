import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from main import app  # Replace with the actual file where your app is defined

client = TestClient(app)

# Test for successfully creating an order with an invoice
@patch("order_service.OrderService.create_order", new_callable=AsyncMock)
@patch("database.fetch_one", new_callable=AsyncMock)
@patch("services.invoice_service.InvoiceService._create_invoice_html", new_callable=MagicMock)
@patch("services.invoice_service.InvoiceService.generate_invoice", new_callable=MagicMock)
@patch("mailing_service.MailingService.send_invoice_email", new_callable=MagicMock)
def test_create_order_with_invoice(
    mock_send_email,
    mock_generate_invoice,
    mock_create_invoice_html,
    mock_fetch_one,
    mock_create_order,
):
    # Mocking the order creation response
    mock_create_order.return_value = {"orderid": 123}

    # Mocking the database user query
    mock_fetch_one.return_value = {"name": "John Doe", "email": "john.doe@example.com"}

    # Mocking the invoice HTML creation
    mock_create_invoice_html.return_value = "<html>Invoice HTML Content</html>"

    # Mocking the invoice PDF generation
    mock_generate_invoice.return_value = "invoices/INV-123.pdf"

    # Mocking email sending (no return value needed)
    mock_send_email.return_value = None

    # Order data for the test
    order_data = {
        "userid": 1,
        "totalamount": 150.0,
        "items": [
            {"productid": 101, "quantity": 2, "price": 50.0},
            {"productid": 102, "quantity": 1, "price": 50.0},
        ],
    }

    # Sending the request
    response = client.post("/create_order_with_invoice", json=order_data)

    # Assertions
    assert response.status_code == 200
    assert response.json()["message"] == "Order created successfully"
    assert response.json()["orderid"] == 123
    assert "<html>Invoice HTML Content</html>" in response.json()["invoice_html"]

    # Verifying that the mocked methods were called
    mock_create_order.assert_called_once_with(order_data)
    mock_fetch_one.assert_called_once_with(
        "SELECT name, email FROM users WHERE userid = :userid", {"userid": 1}
    )
    mock_create_invoice_html.assert_called_once()
    mock_generate_invoice.assert_called_once()
    mock_send_email.assert_called_once_with("john.doe@example.com", "invoices/INV-123.pdf")


# Test for user not found
@patch("database.fetch_one", new_callable=AsyncMock)
def test_create_order_user_not_found(mock_fetch_one):
    # Mocking the database user query to return None
    mock_fetch_one.return_value = None

    # Order data for the test
    order_data = {
        "userid": 999,  # Non-existent user ID
        "totalamount": 150.0,
        "items": [
            {"productid": 101, "quantity": 2, "price": 50.0},
        ],
    }

    # Sending the request
    response = client.post("/create_order_with_invoice", json=order_data)

    # Assertions
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# Test for order creation failure
@patch("order_service.OrderService.create_order", new_callable=AsyncMock)
def test_create_order_failure(mock_create_order):
    # Mocking order creation to raise an exception
    mock_create_order.side_effect = Exception("Failed to create order")

    # Order data for the test
    order_data = {
        "userid": 1,
        "totalamount": 150.0,
        "items": [
            {"productid": 101, "quantity": 2, "price": 50.0},
        ],
    }

    # Sending the request
    response = client.post("/create_order_with_invoice", json=order_data)

    # Assertions
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to create order"
