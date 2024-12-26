import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

# Test for adding an item to the cart
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_add_to_cart(mock_execute, mock_fetch_one):
    # Mock product and cart data
    mock_fetch_one.side_effect = [
        {"productid": 1, "stock": 10},  # Product exists with stock
        None  # Item not in the cart
    ]
    mock_execute.return_value = None  # Mock successful execution

    response = client.post("/cart/add", json={"userid": 1, "productid": 1, "quantity": 2})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to cart successfully."}

# Test for adding an item when product is out of stock
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_add_to_cart_out_of_stock(mock_fetch_one):
    mock_fetch_one.return_value = {"productid": 1, "stock": 0}  # No stock

    response = client.post("/cart/add", json={"userid": 1, "productid": 1, "quantity": 1})

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Product is out of stock"}

# Test for increasing item quantity in the cart
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_increase_cart(mock_execute, mock_fetch_one):
    mock_fetch_one.side_effect = [
        {"stock": 10},  # Product stock
        {"productid": 1, "quantity": 5}  # Cart item exists
    ]

    response = client.post("/cart/increase", params={"userid": 1, "productid": 1})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Quantity increased by 1."}

# Test for increasing quantity beyond stock
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_increase_cart_insufficient_stock(mock_fetch_one):
    mock_fetch_one.side_effect = [
        {"stock": 5},  # Product stock
        {"productid": 1, "quantity": 5}  # Current quantity in cart
    ]

    response = client.post("/cart/increase", params={"userid": 1, "productid": 1})

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient stock for this operation"}

# Test for decreasing item quantity in the cart
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_decrease_cart(mock_execute, mock_fetch_one):
    mock_fetch_one.return_value = {"productid": 1, "quantity": 2}  # Cart item exists

    response = client.post("/cart/decrease", params={"userid": 1, "productid": 1})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Quantity decreased by 1."}

# Test for decreasing quantity below 1
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_decrease_cart_minimum_quantity(mock_fetch_one):
    mock_fetch_one.return_value = {"productid": 1, "quantity": 1}  # Minimum quantity

    response = client.post("/cart/decrease", params={"userid": 1, "productid": 1})

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity cannot be less than 1"}

# Test for removing an item from the cart
@patch("cart_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("cart_endpoints.database.execute", new_callable=AsyncMock)
def test_remove_cart_item(mock_execute, mock_fetch_one):
    mock_fetch_one.return_value = {"productid": 1, "quantity": 2}  # Cart item exists

    response = client.delete("/cart/remove", params={"userid": 1, "productid": 1})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Item removed from cart."}

@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_cart(mock_fetch_all):
    # Mock cart items with the required `image` field
    mock_fetch_all.return_value = [
        {
            "productid": 1,
            "quantity": 2,
            "productname": "Product A",
            "stock": 10,
            "price": 50.00,
            "image": "https://example.com/product-a.jpg"  # Include image
        },
        {
            "productid": 2,
            "quantity": 1,
            "productname": "Product B",
            "stock": 5,
            "price": 30.00,
            "image": "https://example.com/product-b.jpg"  # Include image
        }
    ]

    response = client.get("/cart", params={"userid": 1})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "cart": [
            {
                "productid": 1,
                "productname": "Product A",
                "quantity": 2,
                "stock": 10,
                "price": 50.00,
                "total_price": 100.00,
                "image": "https://example.com/product-a.jpg"
            },
            {
                "productid": 2,
                "productname": "Product B",
                "quantity": 1,
                "stock": 5,
                "price": 30.00,
                "total_price": 30.00,
                "image": "https://example.com/product-b.jpg"
            }
        ],
        "total_cart_price": 130.00
    }


# Test for empty cart
@patch("cart_endpoints.database.fetch_all", new_callable=AsyncMock)
def test_get_cart_empty(mock_fetch_all):
    mock_fetch_all.return_value = []  # No items in cart

    response = client.get("/cart", params={"userid": 1})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Cart is empty", "cart": []}
