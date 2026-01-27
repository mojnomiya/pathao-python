#!/usr/bin/env python3
"""
Error handling example for Pathao Python SDK.

This example demonstrates:
- All exception types
- Proper error handling patterns
- Retry logic
- User-friendly error messages
"""

import os
import time
from pathao import (
    PathaoClient,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
    PathaoException,
)


def demonstrate_authentication_error():
    """Demonstrate authentication error handling."""
    print("\n🔐 Testing Authentication Error...")

    try:
        client = PathaoClient(
            client_id="invalid_id",
            client_secret="invalid_secret",
            username="invalid@email.com",
            password="wrong_password",
            environment="sandbox",
        )

        # This will trigger authentication
        _ = client.get_access_token()

    except AuthenticationError as e:
        print(f" Caught AuthenticationError: {e}")
        print("💡 Solution: Check your credentials")
        return "auth_error"

    return "unexpected_success"


def demonstrate_validation_errors(client):
    """Demonstrate validation error handling."""
    print("\n📝 Testing Validation Errors...")

    validation_tests = [
        {
            "name": "Invalid phone number",
            "data": {
                "store_name": "Test Store",
                "contact_name": "John Doe",
                "contact_number": "123",  # Too short
                "address": "123 Test Street, Dhaka",
                "city_id": 1,
                "zone_id": 1,
                "area_id": 1,
            },
        },
        {
            "name": "Invalid store name",
            "data": {
                "store_name": "AB",  # Too short
                "contact_name": "John Doe",
                "contact_number": "01712345678",
                "address": "123 Test Street, Dhaka",
                "city_id": 1,
                "zone_id": 1,
                "area_id": 1,
            },
        },
    ]

    for test in validation_tests:
        try:
            client.stores.create(**test["data"])
            print(f"❌ Expected validation error for: {test['name']}")

        except ValidationError as e:
            print(f" Caught ValidationError for {test['name']}: {e}")
            if hasattr(e, "field"):
                print(f"   Field: {e.field}")
            if hasattr(e, "value"):
                print(f"   Value: {e.value}")


def demonstrate_not_found_errors(client):
    """Demonstrate not found error handling."""
    print("\n🔍 Testing Not Found Errors...")

    not_found_tests = [
        {"name": "Non-existent store", "func": lambda: client.stores.get(999999)},
        {
            "name": "Non-existent order",
            "func": lambda: client.orders.get_info("INVALID-CONSIGNMENT-ID"),
        },
        {
            "name": "Invalid city zones",
            "func": lambda: client.locations.get_zones(999999),
        },
    ]

    for test in not_found_tests:
        try:
            test["func"]()
            print(f"❌ Expected not found error for: {test['name']}")

        except NotFoundError as e:
            print(f" Caught NotFoundError for {test['name']}: {e}")
            if hasattr(e, "resource_type"):
                print(f"   Resource type: {e.resource_type}")
            if hasattr(e, "resource_id"):
                print(f"   Resource ID: {e.resource_id}")


def demonstrate_configuration_error():
    """Demonstrate configuration error handling."""
    print("\n⚙️ Testing Configuration Error...")

    try:
        _ = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test@example.com",
            password="test_password",
            environment="invalid_environment",  # Invalid environment
        )
        print("❌ Expected configuration error")

    except ConfigurationError as e:
        print(f" Caught ConfigurationError: {e}")
        if hasattr(e, "config_key"):
            print(f"   Config key: {e.config_key}")


def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with comprehensive error handling."""
    try:
        return {"success": True, "data": func(*args, **kwargs)}

    except AuthenticationError as e:
        return {
            "success": False,
            "error_type": "authentication",
            "message": "Authentication failed. Please check your credentials.",
            "details": str(e),
        }

    except ValidationError as e:
        return {
            "success": False,
            "error_type": "validation",
            "message": f"Invalid input: {e}",
            "field": getattr(e, "field", None),
            "details": str(e),
        }

    except NotFoundError as e:
        return {
            "success": False,
            "error_type": "not_found",
            "message": f"Resource not found: {e}",
            "resource_type": getattr(e, "resource_type", None),
            "details": str(e),
        }

    except APIError as e:
        return {
            "success": False,
            "error_type": "api",
            "message": f"Server error: {e}",
            "status_code": getattr(e, "status_code", None),
            "details": str(e),
        }

    except NetworkError as e:
        return {
            "success": False,
            "error_type": "network",
            "message": "Network connection issue. Please check your internet.",
            "retry_count": getattr(e, "retry_count", None),
            "details": str(e),
        }

    except PathaoException as e:
        return {
            "success": False,
            "error_type": "pathao",
            "message": f"Pathao SDK error: {e}",
            "details": str(e),
        }

    except Exception as e:
        return {
            "success": False,
            "error_type": "unexpected",
            "message": f"Unexpected error: {e}",
            "details": str(e),
        }


def retry_with_backoff(func, max_retries=3, base_delay=1, *args, **kwargs):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)

        except (NetworkError, APIError):
            if attempt == max_retries - 1:
                raise  # Last attempt, re-raise

            delay = base_delay * (2**attempt)
            print(f"⏳ Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)

        except Exception:
            # Don't retry for other types of errors
            raise


def demonstrate_safe_api_calls(client):
    """Demonstrate safe API call wrapper."""
    print("\n🛡️ Testing Safe API Call Wrapper...")

    # Test successful call
    result = safe_api_call(client.locations.get_cities)
    if result["success"]:
        print(f" Successful API call: Got {len(result['data'].data)} cities")
    else:
        print(f"❌ API call failed: {result['message']}")

    # Test validation error
    result = safe_api_call(
        client.stores.create,
        store_name="AB",  # Too short
        contact_name="John Doe",
        contact_number="01712345678",
        address="123 Test Street",
        city_id=1,
        zone_id=1,
        area_id=1,
    )

    if not result["success"] and result["error_type"] == "validation":
        print(f" Validation error handled: {result['message']}")
        if result["field"]:
            print(f"   Problem field: {result['field']}")


def demonstrate_retry_logic(client):
    """Demonstrate retry logic."""
    print("\n🔄 Testing Retry Logic...")

    try:
        # This should work normally
        cities = retry_with_backoff(client.locations.get_cities, max_retries=2)
        print(f" Retry logic test passed: Got {len(cities.data)} cities")

    except Exception as e:
        print(f"❌ Retry logic failed: {e}")


def main():
    """Error handling demonstration."""
    print("🚨 Pathao Python SDK - Error Handling Example")
    print("=" * 55)

    # Test configuration error
    demonstrate_configuration_error()

    # Test authentication error
    demonstrate_authentication_error()

    # Initialize valid client for other tests
    try:
        client = PathaoClient(
            client_id=os.getenv("PATHAO_CLIENT_ID", "your_client_id"),
            client_secret=os.getenv("PATHAO_CLIENT_SECRET", "your_client_secret"),
            username=os.getenv("PATHAO_USERNAME", "your_email@example.com"),
            password=os.getenv("PATHAO_PASSWORD", "your_password"),
            environment="sandbox",
        )
        print("\n Valid client initialized for testing")

        # Test validation errors
        demonstrate_validation_errors(client)

        # Test not found errors
        demonstrate_not_found_errors(client)

        # Test safe API call wrapper
        demonstrate_safe_api_calls(client)

        # Test retry logic
        demonstrate_retry_logic(client)

    except Exception as e:
        print(f"❌ Could not initialize valid client: {e}")
        print("💡 Set proper credentials in environment variables to test other errors")

    print("🎉 Error handling example completed!")
    print("📚 Key takeaways:")
    print("   - Always catch specific exception types")
    print("   - Provide user-friendly error messages")
    print("   - Implement retry logic for network/API errors")
    print("   - Log errors for debugging while showing clean messages to users")
    print("   - Validate inputs before making API calls when possible")


if __name__ == "__main__":
    main()
