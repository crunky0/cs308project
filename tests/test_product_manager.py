# tests/test_product_manager_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # or wherever your FastAPI app is defined

client = TestClient(app)



#########################
#   PRODUCTS
#########################

@patch("product_manager_endpoints.database.fetch_val", new_callable=AsyncMock)
@patch("product_manager_endpoints.product_manager_required", return_value=42)
def test_add_product_success(mock_pm_required, mock_fetch_val):
    """
    Test adding a product. Mocks DB insert returning product_id=999
    """
    mock_fetch_val.return_value = 999

    # Sample product data matching ProductCreate model
    product_data = {
        "serialnumber": 12345,
        "productname": "Test Product",
        "productmodel": "Model X",
        "description": "Test Description",
        "distributerinfo": "XYZ Dist",
        "warranty": "1 year",
        "price": 99.99,
        "cost": 50.0,
        "stock": 10,
        "categoryid": 1,
        "soldamount": 0,
        "discountprice": None,
        "image": "test.jpg"
    }

    response = client.post("/productmanagerpanel/products", json=product_data)
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Product added successfully",
        "product_id": 999
    }


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
@patch("product_manager_endpoints.product_manager_required", return_value=42)
def test_remove_product_success(mock_pm_required, mock_execute, mock_fetch_one):
    """
    Test removing a product that exists.
    """
    # The "find_product.sql" returns a row -> product found
    mock_fetch_one.return_value = {"productid": 123}

    response = client.delete("/productmanagerpanel/products/123")
    assert response.status_code == 200
    assert response.json() == {"detail": "Product removed successfully"}


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.product_manager_required", return_value=42)
def test_remove_product_not_found(mock_pm_required, mock_fetch_one):
    """
    Test removing a product that doesn't exist -> 404
    """
    mock_fetch_one.return_value = None

    response = client.delete("/productmanagerpanel/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_update_product_stock_success(mock_execute, mock_fetch_one):
    """
    Test updating a product stock that exists -> success
    """
    # The "find_product.sql" returns a row, so product found
    mock_fetch_one.return_value = {"productid": 1, "stock": 5}

    # Patch out the manager check if you do role checking:
    # or if your route depends on manager, add that patch too

    response = client.patch("/productmanagerpanel/products/1/stock?stock=15")
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Stock updated successfully",
        "new_stock": 15
    }


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_update_product_stock_not_found(mock_fetch_one):
    """
    Test updating stock for a product that doesn't exist -> 404
    """
    mock_fetch_one.return_value = None

    response = client.patch("/productmanagerpanel/products/9999/stock?stock=100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


#########################
#   DELIVERIES
#########################

@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_view_deliveries(mock_fetch_all):
    """
    Test GET /deliveries
    """
    mock_fetch_all.return_value = [
        {"deliveryid": 1, "orderid": 10, "status": "processing"},
        {"deliveryid": 2, "orderid": 11, "status": "in-transit"},
    ]

    response = client.get("/productmanagerpanel/deliveries")
    assert response.status_code == 200
    assert response.json() == {
        "deliveries": [
            {"deliveryid": 1, "orderid": 10, "status": "processing"},
            {"deliveryid": 2, "orderid": 11, "status": "in-transit"}
        ]
    }


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
def test_update_order_status_success(mock_execute, mock_fetch_one):
    """
    Test successfully updating an order status to 'delivered' 
    """
    mock_fetch_one.return_value = {"orderid": 100}  # order found

    response = client.patch("/productmanagerpanel/orders/100/status?status=delivered")
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Order and associated deliveries marked as delivered"
    }


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_update_order_status_not_found(mock_fetch_one):
    """
    Test updating status when order doesn't exist -> 404
    """
    mock_fetch_one.return_value = None

    response = client.patch("/productmanagerpanel/orders/9999/status?status=delivered")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_update_order_status_invalid_status():
    """
    Test invalid status -> 400
    """
    response = client.patch("/productmanagerpanel/orders/100/status?status=unknown")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid status. Must be 'in-transit' or 'delivered'."
    }


@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_create_delivery_success(mock_fetch_all):
    """
    Test creating deliveries for an order. 
    The SQL returns newly inserted rows.
    """
    # Suppose it returns 2 newly inserted deliveries
    mock_fetch_all.return_value = [
        {
            "deliveryid": 10,
            "orderid": 5,
            "customerid": 1,
            "productid": 100,
            "quantity": 2,
            "total_price": 200.0,
            "delivery_address": "123 Street",
            "status": "processing",
            "orderdate": "2023-10-01",
            "price": 100.0,
        },
        {
            "deliveryid": 11,
            "orderid": 5,
            "customerid": 1,
            "productid": 101,
            "quantity": 1,
            "total_price": 50.0,
            "delivery_address": "123 Street",
            "status": "processing",
            "orderdate": "2023-10-01",
            "price": 50.0,
        },
    ]

    payload = {"orderid": 5}
    response = client.post("/productmanagerpanel/deliveries/create", json=payload)
    assert response.status_code == 200

    # Expect a list of deliveries
    data = response.json()
    assert len(data) == 2
    assert data[0]["deliveryid"] == 10
    assert data[1]["productid"] == 101


@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_create_delivery_no_rows(mock_fetch_all):
    """
    Test create_delivery returns no newly inserted rows -> 400
    """
    mock_fetch_all.return_value = []

    payload = {"orderid": 9999}
    response = client.post("/productmanagerpanel/deliveries/create", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "No deliveries were created"}


#########################
#   PROCESSING ORDERS
#########################

@patch("product_manager_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_processing_orders(mock_fetch_all):
    """
    Test retrieving all processing orders.
    The code does two queries: 
      1) fetch_all on the orders
      2) fetch_all on items per order
    We'll mock them in sequence.
    """
    # This approach: we only have one patch for fetch_all. 
    # We can specify a side_effect if multiple queries are called.
    # The code calls fetch_all(orders_query) then fetch_all(items_query)
    # for each order. If there are N orders, it will do N+1 calls total.
    # We'll do a side_effect array, carefully sized.

    # Suppose we have 2 orders in 'processing'
    order_rows = [
        {"orderid": 10, "userid": 1, "totalamount": 120.0, "orderdate": "2023-10-01", "status": "processing"},
        {"orderid": 11, "userid": 2, "totalamount": 75.0, "orderdate": "2023-10-02", "status": "processing"},
    ]
    # Items for orderid=10
    order10_items = [
        {"productid": 1000, "quantity": 2},
        {"productid": 1001, "quantity": 1},
    ]
    # Items for orderid=11
    order11_items = [
        {"productid": 2000, "quantity": 3},
    ]

    # We'll chain them:
    # 1st call to fetch_all -> order_rows
    # 2nd call to fetch_all -> items for order 10
    # 3rd call to fetch_all -> items for order 11
    mock_fetch_all.side_effect = [
        order_rows,
        order10_items,
        order11_items,
    ]

    response = client.get("/productmanagerpanel/orders/processing")
    assert response.status_code == 200
    # We expect 2 orders, each with "items"
    data = response.json()
    assert len(data) == 2

    # Check the first order
    assert data[0]["orderid"] == 10
    assert len(data[0]["items"]) == 2
    assert data[0]["items"][0]["productid"] == 1000

    # Check the second
    assert data[1]["orderid"] == 11
    assert len(data[1]["items"]) == 1


#########################
#   INVOICES
#########################

@patch("product_manager_endpoints.os.path.isdir", return_value=True)
@patch("product_manager_endpoints.os.listdir", return_value=["inv1.pdf", "inv2.PDF", "doc.txt"])
def test_list_invoices(mock_listdir, mock_isdir):
    response = client.get("/productmanagerpanel/invoices")
    assert response.status_code == 200
    # The endpoint filters only PDFs
    # doc.txt not included
    assert response.json() == ["inv1.pdf", "inv2.PDF"]


@patch("product_manager_endpoints.os.path.exists", return_value=True)
def test_get_invoice_success(mock_exists):
    response = client.get("/productmanagerpanel/invoices/my_invoice.pdf")
    assert response.status_code == 200
    # The endpoint returns FileResponse, 
    # so we can't directly compare .json() 
    # We'll check content-disposition
    assert response.headers["content-disposition"] == "inline; filename=my_invoice.pdf"


@patch("product_manager_endpoints.os.path.exists", return_value=False)
def test_get_invoice_not_found(mock_exists):
    response = client.get("/productmanagerpanel/invoices/non_existent.pdf")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invoice not found"}


@patch("product_manager_endpoints.os.path.isdir", return_value=False)
def test_list_invoices_folder_missing(mock_isdir):
    response = client.get("/productmanagerpanel/invoices")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invoices folder not found"}


#########################
#   REVIEWS
#########################

@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.database.execute", new_callable=AsyncMock)
@patch("product_manager_endpoints.product_manager_required", return_value=42)
def test_approve_review_success(mock_pm_required, mock_execute, mock_fetch_one):
    # The review exists
    mock_fetch_one.return_value = {"reviewid": 123}
    response = client.patch("/productmanagerpanel/reviews/123?approved=true")
    assert response.status_code == 200
    assert response.json() == {"detail": "Review approved successfully"}


@patch("product_manager_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("product_manager_endpoints.product_manager_required", return_value=42)
def test_approve_review_not_found(mock_pm_required, mock_fetch_one):
    # The review doesn't exist
    mock_fetch_one.return_value = None

    response = client.patch("/productmanagerpanel/reviews/9999?approved=true")
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found"}
