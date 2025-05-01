import pytest
from unittest.mock import patch
from app.utils.email.sender import send_email


@patch("app.utils.email.sender.configs", new_callable=lambda: {"email": {}})
def test_send_email_empty_config(mock_configs, caplog):
    with caplog.at_level("WARNING"):
        send_email("test@example.com", "Subject", "<p>Body</p>")
        assert "Email configuration not found." in caplog.text


@patch(
    "app.utils.email.sender.configs",
    new_callable=lambda: {
        "email": {
            "PASSWORD": "password123",
            "HOST": "smtp.example.com",
            "PORT": 587,
        }
    },
)
def test_send_email_missing_username(mock_configs):
    with pytest.raises(ValueError) as exc_info:
        send_email("test@example.com", "Subject", "<p>Body</p>")
    assert "email address not found" in str(exc_info.value).lower()


@patch(
    "app.utils.email.sender.configs",
    new_callable=lambda: {
        "email": {
            "USERNAME": "test@example.com",
            "HOST": "smtp.example.com",
            "PORT": 587,
        }
    },
)
def test_send_email_missing_password(mock_configs):
    with pytest.raises(ValueError) as exc_info:
        send_email("test@example.com", "Subject", "<p>Body</p>")
    assert "username or password" in str(exc_info.value).lower()


@patch(
    "app.utils.email.sender.configs",
    new_callable=lambda: {
        "email": {
            "USERNAME": "test@example.com",
            "PASSWORD": "password123",
            # Missing HOST
            "PORT": 587,
        }
    },
)
def test_send_email_missing_host(mock_configs):
    with pytest.raises(ValueError) as exc_info:
        send_email("test@example.com", "Subject", "<p>Body</p>")
    assert "host or port" in str(exc_info.value).lower()


@patch(
    "app.utils.email.sender.configs",
    new_callable=lambda: {
        "email": {
            "USERNAME": "test@example.com",
            "PASSWORD": "password123",
            "HOST": "smtp.example.com",
            # Missing PORT
        }
    },
)
def test_send_email_missing_port(mock_configs):
    with pytest.raises(ValueError) as exc_info:
        send_email("test@example.com", "Subject", "<p>Body</p>")
    assert "host or port" in str(exc_info.value).lower()
