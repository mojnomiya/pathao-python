"""Tests for Pathao SDK validators."""

import pytest
from pathao.validators import (
    validate_name,
    validate_phone,
    validate_address,
    validate_email,
    validate_weight,
    validate_quantity,
    validate_delivery_type,
    validate_item_type,
    validate_integer_range,
)
from pathao.exceptions import ValidationError


class TestValidateName:
    """Test name validation."""

    def test_valid_name(self):
        """Test valid name."""
        result = validate_name("John Doe")
        assert result == "John Doe"

    def test_name_with_whitespace(self):
        """Test name with leading/trailing whitespace."""
        result = validate_name("  John Doe  ")
        assert result == "John Doe"

    def test_name_too_short(self):
        """Test name too short."""
        with pytest.raises(ValidationError) as exc_info:
            validate_name("Jo")
        assert "at least 3 characters" in str(exc_info.value)

    def test_name_too_long(self):
        """Test name too long."""
        long_name = "a" * 51
        with pytest.raises(ValidationError) as exc_info:
            validate_name(long_name)
        assert "not exceed 50 characters" in str(exc_info.value)

    def test_empty_name(self):
        """Test empty name."""
        with pytest.raises(ValidationError):
            validate_name("")

    def test_none_name(self):
        """Test None name."""
        with pytest.raises(ValidationError):
            validate_name(None)


class TestValidatePhone:
    """Test phone validation."""

    def test_valid_phone(self):
        """Test valid phone number."""
        result = validate_phone("01712345678")
        assert result == "01712345678"

    def test_phone_with_formatting(self):
        """Test phone with formatting characters."""
        result = validate_phone("017-123-45678")
        assert result == "01712345678"

    def test_phone_wrong_length(self):
        """Test phone with wrong length."""
        with pytest.raises(ValidationError) as exc_info:
            validate_phone("0171234567")  # 10 digits
        assert "exactly 11 digits" in str(exc_info.value)

    def test_empty_phone(self):
        """Test empty phone."""
        with pytest.raises(ValidationError):
            validate_phone("")

    def test_none_phone(self):
        """Test None phone."""
        with pytest.raises(ValidationError):
            validate_phone(None)


class TestValidateAddress:
    """Test address validation."""

    def test_valid_address(self):
        """Test valid address."""
        address = "House 123, Road 4, Dhaka"
        result = validate_address(address)
        assert result == address

    def test_address_with_whitespace(self):
        """Test address with whitespace."""
        result = validate_address("  House 123, Road 4  ")
        assert result == "House 123, Road 4"

    def test_address_too_short(self):
        """Test address too short."""
        with pytest.raises(ValidationError) as exc_info:
            validate_address("Short")
        assert "at least 10 characters" in str(exc_info.value)

    def test_address_too_long(self):
        """Test address too long."""
        long_address = "a" * 221
        with pytest.raises(ValidationError) as exc_info:
            validate_address(long_address)
        assert "not exceed 220 characters" in str(exc_info.value)


class TestValidateEmail:
    """Test email validation."""

    def test_valid_email(self):
        """Test valid email."""
        result = validate_email("test@example.com")
        assert result == "test@example.com"

    def test_email_case_normalization(self):
        """Test email case normalization."""
        result = validate_email("TEST@EXAMPLE.COM")
        assert result == "test@example.com"

    def test_invalid_email_format(self):
        """Test invalid email format."""
        with pytest.raises(ValidationError) as exc_info:
            validate_email("invalid-email")
        assert "Invalid email format" in str(exc_info.value)

    def test_empty_email(self):
        """Test empty email."""
        with pytest.raises(ValidationError):
            validate_email("")


class TestValidateWeight:
    """Test weight validation."""

    def test_valid_weight_float(self):
        """Test valid weight as float."""
        result = validate_weight(1.5)
        assert result == 1.5

    def test_valid_weight_int(self):
        """Test valid weight as int."""
        result = validate_weight(2)
        assert result == 2.0

    def test_valid_weight_string(self):
        """Test valid weight as string."""
        result = validate_weight("1.5")
        assert result == 1.5

    def test_weight_too_low(self):
        """Test weight too low."""
        with pytest.raises(ValidationError) as exc_info:
            validate_weight(0.3)
        assert "at least 0.5 kg" in str(exc_info.value)

    def test_weight_too_high(self):
        """Test weight too high."""
        with pytest.raises(ValidationError) as exc_info:
            validate_weight(15.0)
        assert "not exceed 10.0 kg" in str(exc_info.value)

    def test_invalid_weight_type(self):
        """Test invalid weight type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_weight("invalid")
        assert "must be a number" in str(exc_info.value)

    def test_none_weight(self):
        """Test None weight."""
        with pytest.raises(ValidationError):
            validate_weight(None)


class TestValidateQuantity:
    """Test quantity validation."""

    def test_valid_quantity_int(self):
        """Test valid quantity as int."""
        result = validate_quantity(5)
        assert result == 5

    def test_valid_quantity_string(self):
        """Test valid quantity as string."""
        result = validate_quantity("3")
        assert result == 3

    def test_quantity_too_low(self):
        """Test quantity too low."""
        with pytest.raises(ValidationError) as exc_info:
            validate_quantity(0)
        assert "at least 1" in str(exc_info.value)

    def test_invalid_quantity_type(self):
        """Test invalid quantity type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_quantity("invalid")
        assert "must be an integer" in str(exc_info.value)


class TestValidateDeliveryType:
    """Test delivery type validation."""

    def test_valid_delivery_type_normal(self):
        """Test valid normal delivery type."""
        result = validate_delivery_type(48)
        assert result == 48

    def test_valid_delivery_type_ondemand(self):
        """Test valid on-demand delivery type."""
        result = validate_delivery_type(12)
        assert result == 12

    def test_valid_delivery_type_string(self):
        """Test valid delivery type as string."""
        result = validate_delivery_type("48")
        assert result == 48

    def test_invalid_delivery_type(self):
        """Test invalid delivery type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_delivery_type(24)
        assert "must be 12 (OnDemand) or 48 (Normal)" in str(exc_info.value)


class TestValidateItemType:
    """Test item type validation."""

    def test_valid_item_type_document(self):
        """Test valid document item type."""
        result = validate_item_type(1)
        assert result == 1

    def test_valid_item_type_parcel(self):
        """Test valid parcel item type."""
        result = validate_item_type(2)
        assert result == 2

    def test_valid_item_type_string(self):
        """Test valid item type as string."""
        result = validate_item_type("1")
        assert result == 1

    def test_invalid_item_type(self):
        """Test invalid item type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_item_type(3)
        assert "must be 1 (Document) or 2 (Parcel)" in str(exc_info.value)


class TestValidateIntegerRange:
    """Test integer range validation."""

    def test_valid_integer_range(self):
        """Test valid integer in range."""
        result = validate_integer_range(5, 1, 10, "test_field")
        assert result == 5

    def test_valid_integer_range_string(self):
        """Test valid integer range as string."""
        result = validate_integer_range("7", 1, 10, "test_field")
        assert result == 7

    def test_integer_below_range(self):
        """Test integer below range."""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer_range(0, 1, 10, "test_field")
        assert "between 1 and 10" in str(exc_info.value)

    def test_integer_above_range(self):
        """Test integer above range."""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer_range(15, 1, 10, "test_field")
        assert "between 1 and 10" in str(exc_info.value)

    def test_invalid_integer_type(self):
        """Test invalid integer type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer_range("invalid", 1, 10, "test_field")
        assert "must be an integer" in str(exc_info.value)
