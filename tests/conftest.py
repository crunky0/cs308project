import pytest
from fastapi.testclient import TestClient
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from main import app
from db import database  # your Database(...) instance

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Connect to the DB at the start of the test session, 
    disconnect at the end. Then TestClient can run queries.
    """
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.connect())   # <-- Connect once

    yield  # run tests

    loop.run_until_complete(database.disconnect())  # <-- Disconnect after all tests


@pytest.fixture
def client():
    """
    A fixture that provides a TestClient for making requests
    """
    with TestClient(app) as c:
        yield c
