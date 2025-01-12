# tests/test_mailing_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # or wherever your FastAPI `app` is defined

client = TestClient(app)

def test_send_invoice_email_success():
    """
    Test the /send_invoice_email endpoint (success scenario).
    
    We'll patch the 'send_invoice_email' method of MailingService 
    so no real email is sent.
    """
    with patch("mailing_service.MailingService.send_invoice_email") as mock_send:
        # Mock the return value from the service
        mock_send.return_value = {"message": "Email sent successfully"}

        # Here, your endpoint's signature is:
        # POST /send_invoice_email?recipient_email=...&invoice_file_path=...
        # We'll pass them as query parameters
        response = client.post(
            "/send_invoice_email",
            params={
                "recipient_email": "customer@example.com",
                "invoice_file_path": "path/to/invoice.pdf"
            }
        )

        assert response.status_code == 200
        # The endpoint returns whatever the service returns
        assert response.json() == {"message": "Email sent successfully"}

        # Optionally verify the mock was called once with the right args
        mock_send.assert_called_once_with(
            "customer@example.com",
            "path/to/invoice.pdf"
        )

def test_send_invoice_email_failure():
    """
    Test the /send_invoice_email endpoint (failure scenario).
    
    We'll mock the service to raise an Exception,
    expecting a 500 response from the endpoint.
    """
    with patch("mailing_service.MailingService.send_invoice_email") as mock_send:
        mock_send.side_effect = Exception("SMTP error")

        response = client.post(
            "/send_invoice_email",
            params={
                "recipient_email": "customer@example.com",
                "invoice_file_path": "path/to/invoice.pdf"
            }
        )

        assert response.status_code == 500
        assert response.json() == {"detail": "SMTP error"}

        # The method was still called once before failing
        mock_send.assert_called_once_with(
            "customer@example.com",
            "path/to/invoice.pdf"
        )
