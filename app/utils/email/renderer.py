from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pathlib import Path

templates_path = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


def render_email_template(template_name: str, context: dict) -> str:
    """
    Render a Jinja2 HTML template for email.
    """
    dummy_request = Request(scope={"type": "http"})
    return templates.get_template(template_name).render(
        {"request": dummy_request, **context}
    )


if __name__ == "__main__":
    # Example usage
    context = {
        "user_name": "Sandile",
        "verification_link": "https://example.com/verify?token=123456",
    }
    html = render_email_template("user_registration.html", context)
    print(html)
    # Example usage
    context = {
        "user_name": "Sandile",
        "otp": "123456",
    }
    html = render_email_template("reset_user_password.html", context)
    print(html)
    # Example usage
    context = {
        "invitee": "John",
        "company": "Oxillium",
        "role": "Engineer",
    }
    html = render_email_template("company_invite.html", context)
    print(html)
    # run command: python -m app.utils.emails.renderer
