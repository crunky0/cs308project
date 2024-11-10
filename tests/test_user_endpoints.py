# tests/test_user_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
from user_endpoints import UserCreate, UserLogin

client = TestClient(app)

# Test for user creation endpoint - success case
@patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("user_endpoints.database.execute", new_callable=AsyncMock)
def test_create_user_success(mock_execute, mock_fetch_one):
    # Configure mock to simulate no existing user
    mock_fetch_one.return_value = None

    # Mock data for creating a new user
    user_data = {
        "username": "newuser",
        "password": "securepassword123",
        "name": "John",
        "surname": "Doe",
        "email": "newuser@example.com"
    }

    # Send POST request to the user registration endpoint
    response = client.post("/users/register/", json=user_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
    mock_execute.assert_called_once()  # Ensure execute was called once

# Test for user creation endpoint - existing username
@patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
def test_create_user_existing_username(mock_fetch_one):
    # Configure mock to simulate existing user
    mock_fetch_one.return_value = {"username": "newuser"}

    # Mock data for creating a user with an existing username
    user_data = {
        "username": "newuser",
        "password": "securepassword123",
        "name": "John",
        "surname": "Doe",
        "email": "newuser@example.com"
    }

    # Send POST request to the user registration endpoint
    response = client.post("/users/register/", json=user_data)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or email already exists"}

# Test for user login endpoint - success case
@patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("user_endpoints.verify_password", return_value=True)
def test_login_success(mock_verify_password, mock_fetch_one):
    # Configure mock to simulate existing user
    mock_fetch_one.return_value = {
        "username": "testuser",
        "password": "hashedpassword123"  # This would be the hashed password in the DB
    }

    # Mock data for logging in
    login_data = {
        "username": "testuser",
        "password": "securepassword123"
    }

    # Send POST request to the login endpoint
    response = client.post("/users/login/", json=login_data)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful", "user": "testuser"}
    mock_verify_password.assert_called_once()  # Ensure password verification was called

# Test for user login endpoint - invalid credentials
@patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
@patch("user_endpoints.verify_password", return_value=False)
def test_login_invalid_credentials(mock_verify_password, mock_fetch_one):
    # Configure mock to simulate existing user but with an incorrect password
    mock_fetch_one.return_value = {
        "username": "testuser",
        "password": "hashedpassword123"
    }

    # Mock data for logging in
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    # Send POST request to the login endpoint
    response = client.post("/users/login/", json=login_data)

    # Assertions
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}
    mock_verify_password.assert_called_once()


