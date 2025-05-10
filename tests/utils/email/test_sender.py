import pytest
from unittest.mock import patch, MagicMock
from app.utils.email.sender import send_email  # Adjust if your file path is different

def test_send_email_in_test_environment(capfd):
    """Should print email body in plain text when environment is test"""
    fake_config = {"environment": "test_environment", "email": {}}

    with patch("app.utils.config.loader.ConfigLoader.get_config", return_value=fake_config):
        send_email("test@example.com", "Test Subject", "<h1>Hello</h1><p>This is a test</p>")
        out, _ = capfd.readouterr()
        assert "Hello" in out
        assert "This is a test" in out

def test_send_email_missing_username():
    """Should raise error if email username is missing"""
    fake_config = {
        "environment": "prod",
        "email": {"PASSWORD": "pass", "HOST": "smtp.test.com", "PORT": 587},
    }

    with patch("app.utils.config.loader.ConfigLoader.get_config", return_value=fake_config):
        with pytest.raises(ValueError, match="Email address not found"):
            send_email("to@example.com", "Subject", "<p>body</p>")

def test_send_email_missing_password():
    """Should raise error if password is missing"""
    fake_config = {
        "environment": "prod",
        "email": {"USERNAME": "user@test.com", "HOST": "smtp.test.com", "PORT": 587},
    }

    with patch("app.utils.config.loader.ConfigLoader.get_config", return_value=fake_config):
        with pytest.raises(ValueError, match="username or password"):
            send_email("to@example.com", "Subject", "<p>body</p>")

def test_send_email_missing_host_or_port():
    """Should raise error if host or port is missing"""
    fake_config = {
        "environment": "prod",
        "email": {"USERNAME": "user@test.com", "PASSWORD": "secure"},
    }

    with patch("app.utils.config.loader.ConfigLoader.get_config", return_value=fake_config):
        with pytest.raises(ValueError, match="host or port"):
            send_email("to@example.com", "Subject", "<p>body</p>")

def test_send_email_success():
    """Should send email successfully with full config"""
    fake_config = {
        "environment": "prod",
        "email": {
            "USERNAME": "user@test.com",
            "PASSWORD": "secure",
            "HOST": "smtp.test.com",
            "PORT": 587,
        },
    }

    with patch("app.utils.config.loader.ConfigLoader.get_config", return_value=fake_config):
        with patch("smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            send_email("to@example.com", "Subject", "<p>test</p>")

            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("user@test.com", "secure")
            mock_server.send_message.assert_called_once()
