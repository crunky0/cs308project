import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # Adjust if your FastAPI app is in a different module

client = TestClient(app)


# 1) Test: Get product by ID
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_product_by_id(mock_fetch_one):
    # Mock DB response for an existing product
    mock_fetch_one.return_value = {
        "productID": 10,
        "productName": "Mocked Mouse",
        "productModel": "Model-MM1",
        "description": "A mocked mouse",
        "distributerInfo": "Mocked Distributor",
        "warranty": "1 year",
        "price": 29.99,
        "cost": 15.00,
        "stock": 100,
        "categoryID": 2,
        "soldAmount": 0,
        "discountPrice": None,
        "image": "mouse.jpg",
        "serialNumber": 12345
    }

    response = client.get("/products/10/")
    assert response.status_code == 200
    assert response.json() == {
        "productID": 10,
        "productName": "Mocked Mouse",
        "productModel": "Model-MM1",
        "description": "A mocked mouse",
        "distributerInfo": "Mocked Distributor",
        "warranty": "1 year",
        "price": 29.99,
        "cost": 15.00,
        "stock": 100,
        "categoryID": 2,
        "soldAmount": 0,
        "discountPrice": None,
        "image": "mouse.jpg",
        "serialNumber": 12345
    }


@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_get_product_by_id_not_found(mock_fetch_one):
    mock_fetch_one.return_value = None  # product not found

    response = client.get("/products/9999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


# 2) Test: Search products by name
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_search_products_by_name(mock_fetch_all):
    # Mock DB returns multiple products
    mock_fetch_all.return_value = [
        {
            "productID": 1,
            "productName": "Mouse",
            "price": 25.00,
            "stock": 50
        },
        {
            "productID": 2,
            "productName": "Mouse Pad",
            "price": 5.00,
            "stock": 200
        },
    ]

    response = client.get("/products/search/name/?productName=Mouse")
    assert response.status_code == 200
    assert response.json() == [
        {
            "productID": 1,
            "productName": "Mouse",
            "price": 25.00,
            "stock": 50
        },
        {
            "productID": 2,
            "productName": "Mouse Pad",
            "price": 5.00,
            "stock": 200
        },
    ]


# 3) Test: Search products by description
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_search_products_by_description(mock_fetch_all):
    mock_fetch_all.return_value = [
        {
            "productID": 1,
            "productName": "Keyboard",
            "description": "A mechanical keyboard"
        },
        {
            "productID": 2,
            "productName": "Gaming Keyboard",
            "description": "Another mechanical keyboard"
        },
    ]

    response = client.get("/products/search/description/?description=keyboard")
    assert response.status_code == 200
    assert response.json() == [
        {
            "productID": 1,
            "productName": "Keyboard",
            "description": "A mechanical keyboard"
        },
        {
            "productID": 2,
            "productName": "Gaming Keyboard",
            "description": "Another mechanical keyboard"
        }
    ]


# 4) Test: Get all products
@patch("product_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_all_products(mock_fetch_all):
    mock_fetch_all.return_value = [
        {"productID": 1, "productName": "Product A"},
        {"productID": 2, "productName": "Product B"},
    ]

    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [
        {"productID": 1, "productName": "Product A"},
        {"productID": 2, "productName": "Product B"},
    ]


# 5) Test: Add a new product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_product(mock_fetch_one):
    mock_fetch_one.return_value = {
        "productID": 999,
        "serialNumber": 12345,
        "productName": "New Product",
        "productModel": "Model123",
        "description": "Test Description",
        "distributerInfo": "Mock Dist.",
        "warranty": "1 year",
        "price": 100.0,
        "cost": 60.0,
        "stock": 10,
        "categoryID": 3,
        "soldAmount": 0,
        "discountPrice": None,
        "image": "new_product.jpg"
    }

    product_data = {
        "serialnumber": 12345,
        "productname": "New Product",
        "productmodel": "Model123",
        "description": "Test Description",
        "distributerinfo": "Mock Dist.",
        "warranty": "1 year",
        "price": 100.0,
        "cost": 60.0,
        "stock": 10,
        "categoryid": 3,
        "soldamount": 0,
        "discountprice": None,
        "image": "new_product.jpg"
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    # Check the returned product matches the mocked DB result
    assert response.json() == {
        "productID": 999,
        "serialNumber": 12345,
        "productName": "New Product",
        "productModel": "Model123",
        "description": "Test Description",
        "distributerInfo": "Mock Dist.",
        "warranty": "1 year",
        "price": 100.0,
        "cost": 60.0,
        "stock": 10,
        "categoryID": 3,
        "soldAmount": 0,
        "discountPrice": None,
        "image": "new_product.jpg"
    }


# 6) Test: Remove a product
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_product(mock_fetch_one):
    # The SQL returns the removed product info
    mock_fetch_one.return_value = {
        "productID": 12,
        "productName": "Old Mouse",
        "price": 15.00,
        "stock": 5
    }

    response = client.delete("/products/12/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product removed successfully",
        "product": {
            "productID": 12,
            "productName": "Old Mouse",
            "price": 15.00,
            "stock": 5
        },
    }


@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_product_not_found(mock_fetch_one):
    mock_fetch_one.return_value = None  # Not found

    response = client.delete("/products/9999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


# 7) Test: Add discount
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_discount(mock_fetch_one):
    # Mocked product after discount
    mock_fetch_one.return_value = {
        "productID": 10,
        "productName": "Product with Discount",
        "price": 200.0,
        "discountPrice": 150.0
    }

    # JSON body
    discount_data = {"discountPrice": 150.0}

    response = client.put("/products/10/discount/", json=discount_data)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Discount added successfully",
        "product": {
            "productID": 10,
            "productName": "Product with Discount",
            "price": 200.0,
            "discountPrice": 150.0
        },
    }


@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_discount_invalid_price(mock_fetch_one):
    """
    Test passing a discountPrice <= 0 -> 400
    """
    # We don't even care about DB here, because
    # the code raises 400 before DB if discount <= 0
    # So let's just mock something
    mock_fetch_one.return_value = None  # won't matter

    discount_data = {"discountPrice": 0.0}
    response = client.put("/products/10/discount/", json=discount_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Discount price must be greater than 0"}


@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_discount_not_found(mock_fetch_one):
    """
    If product not found in DB after trying to add discount -> 404
    """
    mock_fetch_one.return_value = None  # product not found in DB

    discount_data = {"discountPrice": 99.99}
    response = client.put("/products/9999/discount/", json=discount_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


# 8) Test: Remove discount
@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_discount(mock_fetch_one):
    mock_fetch_one.return_value = {
        "productID": 10,
        "productName": "Discounted Product",
        "price": 200.0,
        "discountPrice": None
    }

    response = client.put("/products/10/discount/remove/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Discount removed successfully",
        "product": {
            "productID": 10,
            "productName": "Discounted Product",
            "price": 200.0,
            "discountPrice": None
        },
    }


@patch("product_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_discount_not_found(mock_fetch_one):
    mock_fetch_one.return_value = None  # product doesn't exist

    response = client.put("/products/9999/discount/remove/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
