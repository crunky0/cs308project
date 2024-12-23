import pytest
from main import app 
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


client = TestClient(app)

############################################################
# Sample Data
############################################################
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

stock_update_data = {
    "stock": 15
}

review_approval_data = {
    "approved": True
}

############################################################
# 1) Test Add Product
############################################################

# Successful add product
@patch("product_manager_endpoints.database.fetch_val", new_callable=AsyncMock)
def test_add_product_success(mock_fetch_val):
    """
    Test a successful product creation.
    We patch `fetch_val` because in the code, you likely do:
        productid = await db.fetch_val(query, values)
    """
    # Mock the RETURNING productid from the DB
    mock_fetch_val.return_value = 123

    response = client.post("/productmanagerpanel/products", json=product_data)

    assert response.status_code == 200
    # The endpoint returns {"detail": "Product added successfully", "product_id": productid}
    assert response.json() == {
        "detail": "Product added successfully",
        "product_id": 123
    }

# Database error when adding product
@patch("product_manager_endpoints.database.fetch_val", new_callable=AsyncMock)
def test_add_product_db_error(mock_fetch_val):
    """
    Test scenario where there's a DB error during product insert.
    """
    mock_fetch_val.side_effect = Exception("Database error")

    response = client.post("/productmanagerpanel/products", json=product_data)

    # Assuming your code catches Exception and raises HTTP 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Database error"}

############################################################
# 2) Test Remove Product
############################################################

# Successful remove product
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_product_success(mock_execute, mock_fetch_one):
    """
    Test removing a product successfully.
    We patch fetch_one to simulate product found,
    and patch execute to simulate a successful delete.
    """
    mock_fetch_one.return_value = {"productid": 999}  # product exists

    response = client.delete("/productmanagerpanel/products/999")
    assert response.status_code == 200
    assert response.json() == {"detail": "Product removed successfully"}

# Product not found case
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_product_not_found(mock_fetch_one):
    """
    Test scenario where product doesn't exist in DB.
    """
    mock_fetch_one.return_value = None  # product not found

    response = client.delete("/productmanagerpanel/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

############################################################
# 3) Test Update Product Stock
############################################################

# Successful stock update
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_update_product_stock_success(mock_execute, mock_fetch_one):
    # Mock existing product (e.g., stock=10)
    mock_fetch_one.return_value = {"stock": 10}

    response = client.patch("/productmanagerpanel/products/999/stock", json=stock_update_data)
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Stock updated successfully",
        "new_stock": 15
    }

# Negative stock update
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_update_product_stock_negative(mock_fetch_one):
    """
    If the client tries to set stock to a negative value, 
    your code likely returns 400 or similar.
    """
    mock_fetch_one.return_value = {"stock": 10}  # product found
    response = client.patch("/productmanagerpanel/products/999/stock", json={"stock": -5})
    assert response.status_code == 400
    # Example error from your code: "Stock cannot be negative"
    assert response.json() == {"detail": "Stock cannot be negative"}

############################################################
# 4) Test Approve or Disapprove Review
############################################################

# Successful approval
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_approve_review_success(mock_execute, mock_fetch_one):
    # Simulate review found
    mock_fetch_one.return_value = {"reviewid": 123}

    response = client.patch("/productmanagerpanel/reviews/123", json=review_approval_data)
    assert response.status_code == 200
    assert response.json() == {"detail": "Review approved successfully"}

# Review not found
@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_approve_review_not_found(mock_fetch_one):
    mock_fetch_one.return_value = None  # no review found

    response = client.patch("/productmanagerpanel/reviews/999", json=review_approval_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found"}

############################################################
# 5) Test View Invoices
############################################################

# Example test for GET /invoices
@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_invoices(mock_fetch_all):
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
    response = client.get("/productmanagerpanel/invoices")
    assert response.status_code == 200

    # Example response if your endpoint returns List[InvoiceRead]
    data = response.json()
    assert len(data) == 2
    assert data[0]["invoiceid"] == 1
    assert data[1]["invoice_number"] == "INV-002"
