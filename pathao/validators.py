"""Input validators for Pathao Python SDK."""

import re
from typing import Union

from .exceptions import ValidationError


def validate_name(value: str, min_length: int = 3, max_length: int = 50) -> str:
    """Validate name field."""
    if not value or not isinstance(value, str):
        raise ValidationError("name", "Name is required and must be a string")

    value = value.strip()
    if len(value) < min_length:
        raise ValidationError(
            "name", f"Name must be at least {min_length} characters long"
        )

    if len(value) > max_length:
        raise ValidationError("name", f"Name must not exceed {max_length} characters")

    return value


def validate_phone(value: str, length: int = 11) -> str:
    """Validate phone number."""
    if not value or not isinstance(value, str):
        raise ValidationError("phone", "Phone number is required and must be a string")

    # Remove any non-digit characters
    phone = re.sub(r"\D", "", value)

    if len(phone) != length:
        raise ValidationError("phone", f"Phone number must be exactly {length} digits")

    return phone


def validate_address(value: str, min_length: int = 10, max_length: int = 220) -> str:
    """Validate address field."""
    if not value or not isinstance(value, str):
        raise ValidationError("address", "Address is required and must be a string")

    value = value.strip()
    if len(value) < min_length:
        raise ValidationError(
            "address", f"Address must be at least {min_length} characters long"
        )

    if len(value) > max_length:
        raise ValidationError(
            "address", f"Address must not exceed {max_length} characters"
        )

    return value


def validate_email(value: str) -> str:
    """Validate email address."""
    if not value or not isinstance(value, str):
        raise ValidationError("email", "Email is required and must be a string")

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, value):
        raise ValidationError("email", "Invalid email format")

    return value.lower()


def validate_weight(
    value: Union[int, float], min_weight: float = 0.5, max_weight: float = 10.0
) -> float:
    """Validate weight field."""
    if value is None:
        raise ValidationError("weight", "Weight is required")

    try:
        weight = float(value)
    except (TypeError, ValueError):
        raise ValidationError("weight", "Weight must be a number")

    if weight < min_weight:
        raise ValidationError("weight", f"Weight must be at least {min_weight} kg")

    if weight > max_weight:
        raise ValidationError("weight", f"Weight must not exceed {max_weight} kg")

    return weight


def validate_quantity(value: Union[int, str]) -> int:
    """Validate quantity field."""
    if value is None:
        raise ValidationError("quantity", "Quantity is required")

    try:
        quantity = int(value)
    except (TypeError, ValueError):
        raise ValidationError("quantity", "Quantity must be an integer")

    if quantity < 1:
        raise ValidationError("quantity", "Quantity must be at least 1")

    return quantity


def validate_delivery_type(value: Union[int, str]) -> int:
    """Validate delivery type."""
    if value is None:
        raise ValidationError("delivery_type", "Delivery type is required")

    try:
        delivery_type = int(value)
    except (TypeError, ValueError):
        raise ValidationError("delivery_type", "Delivery type must be an integer")

    if delivery_type not in [12, 48]:
        raise ValidationError(
            "delivery_type", "Delivery type must be 12 (OnDemand) or 48 (Normal)"
        )

    return delivery_type


def validate_item_type(value: Union[int, str]) -> int:
    """Validate item type."""
    if value is None:
        raise ValidationError("item_type", "Item type is required")

    try:
        item_type = int(value)
    except (TypeError, ValueError):
        raise ValidationError("item_type", "Item type must be an integer")

    if item_type not in [1, 2]:
        raise ValidationError(
            "item_type", "Item type must be 1 (Document) or 2 (Parcel)"
        )

    return item_type


def validate_integer_range(
    value: Union[int, str], min_val: int, max_val: int, field_name: str
) -> int:
    """Validate integer within range."""
    if value is None:
        raise ValidationError(field_name, f"{field_name} is required")

    try:
        int_value = int(value)
    except (TypeError, ValueError):
        raise ValidationError(field_name, f"{field_name} must be an integer")

    if int_value < min_val or int_value > max_val:
        raise ValidationError(
            field_name, f"{field_name} must be between {min_val} and {max_val}"
        )

    return int_value
