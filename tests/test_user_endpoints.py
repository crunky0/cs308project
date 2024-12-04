import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app
import user_endpoints
import logging # Import user_endpoints for consistency

logging.basicConfig(level=logging.INFO)
client = TestClient(app)

# Create a logger
logger = logging.getLogger(__name__)


class TestUserEndpoints:
    # Create a logger
    logger = logging.getLogger(__name__)

    @patch("user_endpoints.hash_password", return_value="hashedpassword123")
    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    @patch("user_endpoints.database.execute", new_callable=AsyncMock)
    def test_create_user_success(self, mock_execute, mock_fetch_one, mock_load_sql_file, mock_hash_password):
        logger.info("Testing create user success")

        # Configure mock to simulate no existing user and then return new user data
        mock_fetch_one.side_effect = [
            None,             # First call to fetch_one (checking existing user)
            {"userid": 1}     # Second call to fetch_one (after inserting new user)
        ]
        mock_execute.return_value = None  # Simulate successful execution

        # Mock data for creating a new user
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

        # Assertions
        logger.info("Asserting response status code")
        assert response.status_code == 200
        logger.info("Asserting response message")
        assert response.json()["message"] == "Signup successful"
        logger.info("Asserting response user id")
        assert response.json()["user"]["userid"] == 1

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_create_user_existing_username(self, mock_fetch_one, mock_load_sql_file):
        logger.info("Testing create user existing username")

        # Configure mock to simulate existing user
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "existinguser",
            "email": "existing@example.com"
        }

        # Mock data for creating a user with an existing username
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

        # Assertions
        logger.info("Asserting response status code")
        assert response.status_code == 400
        logger.info("Asserting response detail")
        assert response.json()["detail"] == "Username or email already exists"

    @patch("user_endpoints.verify_password", return_value=True)
    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_success(self, mock_fetch_one, mock_load_sql_file, mock_verify_password):
        logger.info("Testing login success")

        # Configure mock to simulate existing user
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "testuser",
            "password": "hashedpassword123"
        }

        # Mock data for logging in
        login_data = {
            "username": "testuser",
            "password": "securepassword123"
        }

        response = client.post("/users/login/", json=login_data)

        # Assertions
        logger.info("Asserting response status code")
        assert response.status_code == 200
        logger.info("Asserting response message")
        assert response.json()["message"] == "Login successful"
        logger.info("Asserting response user id")
        assert response.json()["user"]["userid"] == 1

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_invalid_credentials(self, mock_fetch_one, mock_load_sql_file):
        logger.info("Testing login invalid credentials")

        # Configure mock to simulate no matching user
        mock_fetch_one.return_value = None

        # Mock data for logging in with invalid credentials
        login_data = {
            "username": "invaliduser",
            "password": "wrongpassword"
        }

        response = client.post("/users/login/", json=login_data)

        # Assertions
        logger.info("Asserting response status code")
        assert response
        # Mock data for creating a new user
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

        # Assertions
        assert response.status_code == 200
        assert response.json()["message"] == "Signup successful"
        assert response.json()["user"]["userid"] == 1

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_create_user_existing_username(self, mock_fetch_one, mock_load_sql_file):
        # Correct order of arguments: mock_fetch_one, mock_load_sql_file

        # Configure mock to simulate existing user
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "existinguser",
            "email": "existing@example.com"
        }

        # Mock data for creating a user with an existing username
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

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "Username or email already exists"

    @patch("user_endpoints.verify_password", return_value=True)
    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_success(self, mock_fetch_one, mock_load_sql_file, mock_verify_password):
        # Correct order of arguments: mock_fetch_one, mock_load_sql_file, mock_verify_password

        # Configure mock to simulate existing user
        mock_fetch_one.return_value = {
            "userid": 1,
            "username": "testuser",
            "password": "hashedpassword123"
        }

        # Mock data for logging in
        login_data = {
            "username": "testuser",
            "password": "securepassword123"
        }

        response = client.post("/users/login/", json=login_data)

        # Assertions
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"
        assert response.json()["user"]["userid"] == 1

    @patch("user_endpoints.load_sql_file", return_value="DUMMY SQL QUERY")
    @patch("user_endpoints.database.fetch_one", new_callable=AsyncMock)
    def test_login_invalid_credentials(self, mock_fetch_one, mock_load_sql_file):
        # Correct order of arguments: mock_fetch_one, mock_load_sql_file

        # Configure mock to simulate no matching user
        mock_fetch_one.return_value = None

        # Mock data for logging in with invalid credentials
        login_data = {
            "username": "invaliduser",
            "password": "wrongpassword"
        }

        response = client.post("/users/login/", json=login_data)

        # Assertions
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"
