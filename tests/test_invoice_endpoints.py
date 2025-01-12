# tests/test_invoice_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # or wherever your FastAPI `app` is defined

client = TestClient(app)

def test_generate_invoice_success():
    """
    Test a successful invoice generation.
    We patch the InvoiceService methods so no real PDF is generated.
    """
    # Mock request JSON
    request_body = {
        "user_info": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        "items": [
            {"name": "Product 1", "quantity": 2, "price": 10.0},
            {"name": "Product 2", "quantity": 1, "price": 25.0},
        ],
        "total_amount": 45.0
    }

    # We'll patch 'services.invoice_service.InvoiceService' so that:
    # 1) _create_invoice_html(...) returns a dummy HTML
    # 2) generate_invoice(...) returns a dummy file path
    with patch("services.invoice_service.InvoiceService._create_invoice_html") as mock_html, \
         patch("services.invoice_service.InvoiceService.generate_invoice") as mock_gen:
        
        mock_html.return_value = "<html><body>Dummy Invoice</body></html>"
        mock_gen.return_value = "invoices/INV-12345.pdf"

        response = client.post("/generate-invoice", json=request_body)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Invoice generated successfully"
        assert data["file_path"] == "invoices/INV-12345.pdf"

        # Optionally, verify the mocked calls
        mock_html.assert_called_once()
        mock_gen.assert_called_once()

def test_generate_invoice_failure():
    """
    Test invoice generation fails (e.g., an exception is raised).
    """
    request_body = {
        "user_info": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        "items": [
            {"name": "Product 1", "quantity": 2, "price": 10.0},
        ],
        "total_amount": 20.0
    }

    with patch("services.invoice_service.InvoiceService._create_invoice_html") as mock_html, \
         patch("services.invoice_service.InvoiceService.generate_invoice") as mock_gen:
        
        # Suppose generate_invoice(...) raises an error
        mock_html.return_value = "<html><body>Dummy Invoice</body></html>"
        mock_gen.side_effect = Exception("PDF generation error")

        response = client.post("/generate-invoice", json=request_body)

        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "PDF generation error"
        
        # Check calls
        mock_html.assert_called_once()
        mock_gen.assert_called_once()
