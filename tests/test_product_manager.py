# tests/test_product_manager.py

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Ensure Python can find your main module
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from main import app  # Adjust if needed for your project structure

client = TestClient(app)

# Sample data for testing
product_data = {
    "categoryid": 1,
    "productname": "Test Product",
    "productmodel": "Model X",
    "description": "Test Description",
    "distributerinfo": "XYZ Distributer",
    "warranty": "1 year",
    "price": 99.99,
    "stock": 10
}

stock_update_data = {"stock": 15}
review_approval_data = {"approved": True}
DUMMY_HEADERS = {"Authorization": "Bearer test-token"}

###############################################################################
# 1) Test Add Product
###############################################################################
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)             # role check
@patch("product_manager_endpoints.database.fetch_val", new_callable=AsyncMock) # route DB call
def test_add_product_success(mock_fetch_val, mock_dep_fetch_one):
    """
    Test a successful product creation with fully mocked DB calls.
    
    Mocks:
      - `dependencies.db.fetch_one` -> always returns {"role": "Productmanager"}
      - `product_manager_endpoints.db.fetch_val` -> simulates inserted product ID=999
    """
    # The role check sees a user with role=Productmanager
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    # The route-level insert returns product ID=999
    mock_fetch_val.return_value = 999

    response = client.post(
        "/productmanagerpanel/products?user_id=13",  # user_id=13 is a manager
        json=product_data
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Product added successfully",
        "product_id": 999
    }

@patch("dependencies.database.fetch_one", new_callable=AsyncMock)             # role check
@patch("product_manager_endpoints.database.fetch_val", new_callable=AsyncMock) # route DB call
def test_add_product_db_error(mock_fetch_val, mock_dep_fetch_one):
    """
    Test scenario where a DB error occurs during product insert.
    We expect a 400 response with {"detail": "Database error"}.
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    # Simulate a DB error on insert
    mock_fetch_val.side_effect = Exception("Database error")

    response = client.post(
        "/productmanagerpanel/products?user_id=13",
        json=product_data,
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Database error"}

###############################################################################
# 2) Test Remove Product
###############################################################################
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)               # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)   # route check if product exists
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)     # route delete product
def test_remove_product_success(mock_execute, mock_route_fetch_one, mock_dep_fetch_one):
    """
    Test removing a product successfully.
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = {"productid": 999}  # Product found

    response = client.delete(
        "/productmanagerpanel/products/999?user_id=13",
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Product removed successfully"}

@patch("dependencies.database.fetch_one", new_callable=AsyncMock)               # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)   # route check if product exists
def test_remove_product_not_found(mock_route_fetch_one, mock_dep_fetch_one):
    """
    Test removing a product that does not exist -> 404
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = None  # No product found

    response = client.delete(
        "/productmanagerpanel/products/999?user_id=13",
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

###############################################################################
# 3) Test Update Product Stock
###############################################################################
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)                # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)    # route check product
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)      # route update stock
def test_update_product_stock_success(mock_execute, mock_route_fetch_one, mock_dep_fetch_one):
    """
    Test updating stock from 10 to 15 -> success
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = {"stock": 10}  # current stock

    response = client.patch(
        "/productmanagerpanel/products/999/stock?user_id=13",
        json=stock_update_data,
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Stock updated successfully",
        "new_stock": 15
    }

@patch("dependencies.database.fetch_one", new_callable=AsyncMock)               # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)   # route check product
def test_update_product_stock_negative(mock_route_fetch_one, mock_dep_fetch_one):
    """
    Test user tries to set stock to -5 -> 400
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = {"stock": 10}

    response = client.patch(
        "/productmanagerpanel/products/999/stock?user_id=13",
        json={"stock": -5},
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Stock cannot be negative"}

###############################################################################
# 4) Test Approve/Disapprove Review
###############################################################################
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)               # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)   # route check review
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)     # route update review
def test_approve_review_success(mock_execute, mock_route_fetch_one, mock_dep_fetch_one):
    """
    Test approving a found review -> 200
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = {"reviewid": 123}

    response = client.patch(
        "/productmanagerpanel/reviews/123?user_id=13",
        json=review_approval_data,
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Review approved successfully"}
    
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)               # role check
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)   # route check review
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)     # route update review
def test_approve_review_not_found(mock_execute, mock_route_fetch_one, mock_dep_fetch_one):
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_route_fetch_one.return_value = None  # No review -> 404

    response = client.patch(
        "/productmanagerpanel/reviews/999?user_id=13",
        json=review_approval_data,
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found"}


###############################################################################
# 5) Test Get Invoices
###############################################################################
@patch("dependencies.database.fetch_one", new_callable=AsyncMock)                 # role check
@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)    # route get invoices
def test_get_invoices(mock_fetch_all, mock_dep_fetch_one):
    """
    Test listing invoices -> 200
    """
    mock_dep_fetch_one.return_value = {"role": "Productmanager"}
    mock_fetch_all.return_value = [
        {
            "invoiceid": 1,
            "orderid": 10,
            "invoice_number": "INV-001",
            "invoice_date": None,
            "file_path": "path/to/invoice1.pdf",
        },
        {
            "invoiceid": 2,
            "orderid": 12,
            "invoice_number": "INV-002",
            "invoice_date": None,
            "file_path": "path/to/invoice2.pdf",
        },
    ]

    response = client.get(
        "/productmanagerpanel/invoices?user_id=13",
        headers=DUMMY_HEADERS
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["invoiceid"] == 1
    assert data[1]["invoice_number"] == "INV-002"
