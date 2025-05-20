import click
import logging
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
from app.utils.config.email_config import EmailConfig


def send_email(to: str, subject: str, html_body: str):
    email_settings = EmailConfig.load()

    if not email_settings:
        soup = BeautifulSoup(html_body, "html.parser")
        click.echo(click.style("Email config not available. Showing plain text:", fg="yellow"))
        click.echo(soup.get_text(separator="\n", strip=True))
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_settings.username
    msg["To"] = to
    msg.set_content("This email requires an HTML-compatible client.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(host=email_settings.host, port=email_settings.port) as server:
        server.starttls()
        server.login(email_settings.username, email_settings.password)
        server.send_message(msg)



if __name__ == "__main__":
    # Example usage
    to = "as@fg.dsfgd"
    subject = "Test Email"
    html_body = "<h1>Hello</h1><p>This is a test email.</p>"
    send_email(to, subject, html_body)
