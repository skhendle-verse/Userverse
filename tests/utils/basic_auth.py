import base64


def get_basic_auth_header(username: str, password: str) -> dict:
    """
    Generate the Basic Auth header for HTTP requests.

    Args:
        username (str): The username (email).
        password (str): The password.

    Returns:
        dict: A dictionary with the Authorization header.
    """
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}
