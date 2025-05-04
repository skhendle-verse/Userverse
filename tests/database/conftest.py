import pytest
import json
from unittest.mock import patch
from app.utils.configs import ConfigLoader
from app.database import DatabaseSessionManager


@pytest.fixture(scope="session")
def test_data():
    """Fixture to load test data from JSON file."""
    # Load the test data from JSON file
    with open("tests/data/database/user_db_test_data.json") as f:
        data = json.load(f)
    return data


@pytest.fixture(scope="function")
def test_session():
    # Mock the get_config method of ConfigLoader to return an in-memory SQLite DB config
    with patch.object(
        ConfigLoader,
        "get_config",
        return_value={
            "database_url": "sqlite:///:memory:",
            "environment": "test",
            "cor_origins": {"allowed": ["*"], "blocked": []},
            "jwt": {},
            "email": {},
            "version": "0.1.0",
            "name": "Userverse",
            "description": "Mocked config for test",
        },
    ):
        db_manager = DatabaseSessionManager()
        session = db_manager.session_object()
        yield session
        session.close()
