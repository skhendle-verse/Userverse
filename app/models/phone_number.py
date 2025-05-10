import re
from typing import Optional

PHONE_NUMBER_REGEX = re.compile(
    r"^\+?\d{10,15}$"
) 


def validate_phone_number_format(phone: Optional[str]) -> Optional[str]:
    if phone and not PHONE_NUMBER_REGEX.match(phone):
        raise ValueError("Invalid phone number format. Must be 10-15 digits, optional leading '+'.")
    return phone
