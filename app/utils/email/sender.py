import click
import logging
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
import socket
from app.utils.config.email_config import EmailConfig

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, html_body: str):
    email_settings = EmailConfig.load()

    if not email_settings:
        soup = BeautifulSoup(html_body, "html.parser")
        click.echo(
            click.style("Email config not available. Showing plain text:", fg="yellow")
        )
        click.echo(soup.get_text(separator="\n", strip=True))
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_settings.username
    msg["To"] = to
    msg.set_content("This email requires an HTML-compatible client.")
    msg.add_alternative(html_body, subtype="html")

    try:
        logger.info(
            f"Connecting to SMTP server at {email_settings.host}:{email_settings.port}"
        )
        with smtplib.SMTP_SSL(
            email_settings.host,
            email_settings.port,
        ) as smtp:
            smtp.login(
                email_settings.username,
                email_settings.password,
            )
            smtp.send_message(msg)
    except socket.timeout:
        logger.error(
            f"Timeout connecting to SMTP server at {email_settings.host}:{email_settings.port}"
        )
        raise
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"SMTP server disconnected: {str(e)}")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}")
        raise
