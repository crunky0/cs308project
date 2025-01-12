import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app
import logging

logging.basicConfig(level=logging.INFO)
client = TestClient(app)

class TestUserEndpoints:
    logger = logging.getLogger(__name__)

    @patch("user_endpoints.hash_password", return_value="hashedpassword123")
    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    @patch("user_endpoints.database.execute", new_callable=AsyncMock)
    def test_create_user_success(self, mock_execute, mock_fetch_one, mock_load_sql_file, mock_hash_password):
        self.logger.info("Testing create user success")

        # First call: check if user exists (None => no user found)
        # Second call: returns {"userid": 1} after successful insert
        mock_fetch_one.side_effect = [None, {"userid": 1}]
        mock_execute.return_value = None  # successful execute

        user_data = {
            "username": "newuser",
            "password": "securepassword123",
            "name": "John",
            "surname": "Doe",
            "email": "newuser@example.com",
            "taxID": "1234567890",
            "homeAddress": "123 Elm Street"
        }

        response = client.post("/users/register/", json=user_data)

        self.logger.info("Asserting response")
        assert response.status_code == 200
        assert response.json()["message"] == "Signup successful"
        assert response.json()["user"]["userid"] == 1

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_create_user_existing_username(self, mock_fetch_one, mock_load_sql_file):
        self.logger.info("Testing create user existing username")

        # Mock that user already exists
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "existinguser",
            "email": "existing@example.com"
        }

        user_data = {
            "username": "existinguser",
            "password": "securepassword123",
            "name": "John",
            "surname": "Doe",
            "email": "existing@example.com",
            "taxID": "1234567890",
            "homeAddress": "123 Elm Street"
        }

        response = client.post("/users/register/", json=user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Username or email already exists"

    @patch("user_endpoints.verify_password", return_value=True)
    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_success(self, mock_fetch_one, mock_load_sql_file, mock_verify_password):
        self.logger.info("Testing login success")

        # Mock DB user row includes "role" to avoid KeyError
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "testuser",
            "password": "hashedpassword123",
            "role": "customer"  # <-- Added to prevent KeyError('role')
        }

        login_data = {
            "username": "testuser",
            "password": "securepassword123"
        }

        response = client.post("/users/login/", json=login_data)
        assert response.status_code == 200
        json_resp = response.json()
        assert json_resp["message"] == "Login successful"
        assert json_resp["user"]["userid"] == 1
        assert json_resp["user"]["email"] == "testuser"
        assert json_resp["user"]["role"] == "customer"

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_invalid_credentials(self, mock_fetch_one, mock_load_sql_file):
        self.logger.info("Testing login invalid credentials")

        # Mock no matching user in DB
        mock_fetch_one.return_value = None

        login_data = {
            "username": "invaliduser",
            "password": "wrongpassword"
        }

        response = client.post("/users/login/", json=login_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"
