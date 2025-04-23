import hashlib


def hash_password(password: str) -> str:
    """
    Hashes a password using SHA-256 and returns the first 30 characters of the hash.
    """
    return hashlib.md5(password.encode()).hexdigest()[:30]