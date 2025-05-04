import logging
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
from app.utils.configs import ConfigLoader


def send_email(to: str, subject: str, html_body: str):
    # load configs
    loader = ConfigLoader()
    configs = loader.get_config()
    environment = configs.get("environment")
    email_config = configs.get("email", {})

    if not email_config or environment == "test_environment":
        logging.warning("Email configuration not found.")
        soup = BeautifulSoup(html_body, "html.parser")
        print("\n", soup.get_text(separator="\n", strip=True), "\n")
        return

    username = email_config.get("USERNAME")
    password = email_config.get("PASSWORD")
    host = email_config.get("HOST")
    port = email_config.get("PORT")

    if not username:
        raise ValueError("Email address not found in configuration.")
    if not password:
        raise ValueError("Email username or password not found in configuration.")
    if not host or not port:
        raise ValueError("Email host or port not found in configuration.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to
    msg.set_content("This email requires an HTML-compatible client.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(host=host, port=port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
