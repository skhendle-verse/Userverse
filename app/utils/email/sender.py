import logging
from email.message import EmailMessage
import smtplib
from app.configs import configs


def send_email(to: str, subject: str, html_body: str):
    email_config = configs.get("email", {})

    if not email_config:
        logging.warning("Email configuration not found.")
        logging.info("\n%s\n", html_body)
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
