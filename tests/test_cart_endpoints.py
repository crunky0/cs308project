# tests/test_cart_endpoints.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # or wherever your FastAPI app is defined

client = TestClient(app)


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_add_to_cart(mock_execute, mock_fetch_one):
    """
    Test adding a product to the cart when:
     - The product exists and has stock > 0.
     - The cart does not already contain the product.
    """
    # Mock DB call #1 (check product)
    # Mock DB call #2 (check existing cart item -> None)
    mock_fetch_one.side_effect = [
        {"productid": 1, "stock": 10},  # Product found with stock
        None  # No existing cart item
    ]

    # POST request body
    request_body = {
        "userid": 1,
        "productid": 1,
        "quantity": 2
    }

    response = client.post("/cart/add", json=request_body)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to cart successfully."}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_to_cart_product_not_found(mock_fetch_one):
    """
    Test adding to cart with non-existing product -> 404
    """
    mock_fetch_one.return_value = None  # No product found

    request_body = {
        "userid": 1,
        "productid": 999,  # non-existing
        "quantity": 1
    }

    response = client.post("/cart/add", json=request_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_to_cart_out_of_stock(mock_fetch_one):
    """
    Test adding a product that has stock=0 -> 400
    """
    # The first fetch_one() is the product query
    mock_fetch_one.return_value = {"productid": 1, "stock": 0}

    request_body = {
        "userid": 2,
        "productid": 1,
        "quantity": 1
    }

    response = client.post("/cart/add", json=request_body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Product is out of stock"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_increase_cart(mock_execute, mock_fetch_one):
    """
    Test increasing cart quantity by 1 when:
     - Product exists
     - Cart item exists
     - New quantity is within stock
    """
    # DB call #1 -> product stock
    # DB call #2 -> cart item
    mock_fetch_one.side_effect = [
        {"stock": 10},  # product with enough stock
        {"productid": 1, "quantity": 5}  # cart item
    ]

    response = client.post("/cart/increase", params={"userid": 1, "productid": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Quantity increased by 1."}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_increase_cart_insufficient_stock(mock_fetch_one):
    """
    Test increasing cart quantity beyond available stock -> 400
    """
    mock_fetch_one.side_effect = [
        {"stock": 5},  # product stock
        {"productid": 1, "quantity": 5}  # cart item with quantity=5
    ]

    response = client.post("/cart/increase", params={"userid": 1, "productid": 1})
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient stock for this operation"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_increase_cart_item_not_found(mock_fetch_one):
    """
    Test increasing cart when no cart item -> 404
    """
    # DB call #1 -> product stock
    # DB call #2 -> cart item (None)
    mock_fetch_one.side_effect = [
        {"stock": 10},
        None  # cart item not found
    ]

    response = client.post("/cart/increase", params={"userid": 1, "productid": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found in cart"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_decrease_cart(mock_execute, mock_fetch_one):
    """
    Test decreasing cart quantity by 1 when:
     - Cart item exists
     - quantity - 1 >= 1
    """
    mock_fetch_one.return_value = {"productid": 1, "quantity": 2}

    response = client.post("/cart/decrease", params={"userid": 1, "productid": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Quantity decreased by 1."}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_decrease_cart_below_minimum(mock_fetch_one):
    """
    Test decreasing cart item below quantity=1 -> 400
    """
    mock_fetch_one.return_value = {"productid": 1, "quantity": 1}

    response = client.post("/cart/decrease", params={"userid": 1, "productid": 1})
    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity cannot be less than 1"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_decrease_cart_item_not_found(mock_fetch_one):
    """
    Test decreasing cart item that doesn't exist -> 404
    """
    mock_fetch_one.return_value = None  # no cart item

    response = client.post("/cart/decrease", params={"userid": 1, "productid": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found in cart"}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_cart_item(mock_execute, mock_fetch_one):
    """
    Test removing item from cart when it exists
    """
    mock_fetch_one.return_value = {"productid": 1, "quantity": 3}  # cart item found

    response = client.delete("/cart/remove", params={"userid": 1, "productid": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Item removed from cart."}


@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_remove_cart_item_not_found(mock_fetch_one):
    """
    Test removing item from cart when it does not exist -> 404
    """
    mock_fetch_one.return_value = None

    response = client.delete("/cart/remove", params={"userid": 1, "productid": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found in cart"}


@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_cart(mock_fetch_all):
    """
    Test retrieving cart with items
    """
    mock_fetch_all.return_value = [
        {
            "productid": 1,
            "quantity": 2,
            "productname": "Product A",
            "stock": 10,
            "price": 50.00,
            "discountprice": 30.00,
            "image": "https://example.com/a.jpg"
        },
        {
            "productid": 2,
            "quantity": 1,
            "productname": "Product B",
            "stock": 5,
            "price": 25.00,
            "discountprice": None,
            "image": "https://example.com/b.jpg"
        },
    ]

    response = client.get("/cart", params={"userid": 3})
    assert response.status_code == 200

    # First item uses discountprice=30.00
    # => total_price for item 1 = 2 * 30 = 60
    # Second item uses price=25.00 because discountprice=None
    # => total_price for item 2 = 1 * 25 = 25
    # total_cart_price = 60 + 25 = 85
    expected_json = {
        "cart": [
            {
                "productid": 1,
                "productname": "Product A",
                "quantity": 2,
                "stock": 10,
                "price": 50.0,
                "discountprice": 30.0,
                "total_price": 60.0,
                "image": "https://example.com/a.jpg"
            },
            {
                "productid": 2,
                "productname": "Product B",
                "quantity": 1,
                "stock": 5,
                "price": 25.0,
                "discountprice": None,
                "total_price": 25.0,
                "image": "https://example.com/b.jpg"
            },
        ],
        "total_cart_price": 85.0
    }
    assert response.json() == expected_json


@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_cart_empty(mock_fetch_all):
    """
    Test retrieving an empty cart
    """
    mock_fetch_all.return_value = []

    response = client.get("/cart", params={"userid": 3})
    assert response.status_code == 200
    assert response.json() == {"message": "Cart is empty", "cart": []}


@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_empty_cart(mock_execute, mock_fetch_all):
    """
    Test emptying a cart that has items
    """
    # The SELECT query returns some items
    mock_fetch_all.return_value = [
        {"productid": 1, "quantity": 2},
        {"productid": 2, "quantity": 3},
    ]

    response = client.delete("/cart/empty", params={"userid": 5})
    assert response.status_code == 200

    # Expect a list of deleted items in response
    assert response.json() == {
        "message": "Cart has been emptied successfully.",
        "deleted_items": [
            {"productid": 1, "quantity": 2},
            {"productid": 2, "quantity": 3}
        ]
    }


@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_empty_cart_not_found(mock_fetch_all):
    """
    Test emptying an empty cart -> 404
    """
    mock_fetch_all.return_value = []  # no items in cart

    response = client.delete("/cart/empty", params={"userid": 5})
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart is already empty or user does not exist"}
