import pytest
from unittest.mock import AsyncMock
from databases import Database
from order_service import OrderService

# Fixture for mock database
@pytest.fixture
def mock_database():
    db = AsyncMock(spec=Database)
    return db

# Fixture for OrderService with mock database
@pytest.fixture
def order_service(mock_database):
    return OrderService(db=mock_database)
