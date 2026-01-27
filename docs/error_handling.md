# Error Handling

## Overview

The Pathao Python SDK provides comprehensive error handling with specific exception types for different error scenarios.

## Exception Hierarchy

```python
PathaoException                    # Base exception
├── AuthenticationError           # Authentication failures
├── ValidationError              # Input validation errors
├── NotFoundError               # Resource not found
├── APIError                    # API server errors
├── NetworkError                # Network/connection issues
└── ConfigurationError          # Configuration problems
```

## Import Exceptions

```python
from pathao import (
    PathaoException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError
)
```

## Authentication Errors

```python
from pathao import PathaoClient, AuthenticationError

try:
    client = PathaoClient(
        client_id="invalid_id",
        client_secret="invalid_secret",
        username="invalid@email.com",
        password="wrong_password",
        environment="sandbox"
    )

    # This will trigger authentication
    token = client.get_access_token()

except AuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
    # Handle: Show login form, refresh credentials, etc.
```

## Validation Errors

```python
from pathao import ValidationError

try:
    # Invalid phone number
    store = client.stores.create(
        store_name="Test Store",
        contact_name="John Doe",
        contact_number="123",  # Too short
        address="Test Address",
        city_id=1,
        zone_id=1,
        area_id=1
    )
except ValidationError as e:
    print(f"❌ Validation error: {e}")
    print(f"Field: {e.field}")
    print(f"Value: {e.value}")
    # Handle: Show field-specific error message
```

## Not Found Errors

```python
from pathao import NotFoundError

try:
    # Non-existent store
    store = client.stores.get(999999)
except NotFoundError as e:
    print(f"❌ Resource not found: {e}")
    print(f"Resource type: {e.resource_type}")
    print(f"Resource ID: {e.resource_id}")
    # Handle: Show "not found" message, redirect, etc.

try:
    # Non-existent order
    order = client.orders.get_info("INVALID-CONSIGNMENT-ID")
except NotFoundError as e:
    print(f"❌ Order not found: {e}")
```

## API Errors

```python
from pathao import APIError

try:
    order = client.orders.create(
        store_id=123,
        merchant_order_id="ORDER-001",
        recipient_name="John Doe",
        recipient_phone="01712345678",
        recipient_address="Test Address",
        recipient_city=1,
        recipient_zone=1,
        delivery_type=48,
        item_type=2,
        item_quantity=1,
        item_weight=1.0,
        amount_to_collect=100.0
    )
except APIError as e:
    print(f"❌ API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response data: {e.response_data}")
    # Handle: Retry, show server error message, etc.
```

## Network Errors

```python
from pathao import NetworkError

try:
    cities = client.locations.get_cities()
except NetworkError as e:
    print(f"❌ Network error: {e}")
    print(f"Retry count: {e.retry_count}")
    # Handle: Show offline message, retry button, etc.
```

## Configuration Errors

```python
from pathao import ConfigurationError

try:
    client = PathaoClient(
        client_id="test_id",
        client_secret="test_secret",
        username="test@example.com",
        password="test_password",
        environment="invalid_env"  # Invalid environment
    )
except ConfigurationError as e:
    print(f"❌ Configuration error: {e}")
    print(f"Config key: {e.config_key}")
    # Handle: Show configuration help, default values, etc.
```

## Comprehensive Error Handling

```python
from pathao import (
    PathaoClient,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
    PathaoException
)

def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with comprehensive error handling."""
    try:
        return func(*args, **kwargs)

    except AuthenticationError as e:
        print(f"🔐 Authentication issue: {e}")
        return {"error": "auth", "message": str(e)}

    except ValidationError as e:
        print(f"📝 Validation error: {e}")
        return {"error": "validation", "field": e.field, "message": str(e)}

    except NotFoundError as e:
        print(f"🔍 Not found: {e}")
        return {"error": "not_found", "resource": e.resource_type, "message": str(e)}

    except APIError as e:
        print(f"🌐 API error: {e}")
        return {"error": "api", "status": e.status_code, "message": str(e)}

    except NetworkError as e:
        print(f"📡 Network error: {e}")
        return {"error": "network", "retries": e.retry_count, "message": str(e)}

    except ConfigurationError as e:
        print(f"⚙️ Configuration error: {e}")
        return {"error": "config", "key": e.config_key, "message": str(e)}

    except PathaoException as e:
        print(f"❌ Pathao error: {e}")
        return {"error": "pathao", "message": str(e)}

    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return {"error": "unexpected", "message": str(e)}

# Usage examples
def create_order_safely(client, order_data):
    """Create order with comprehensive error handling."""
    result = safe_api_call(
        client.orders.create,
        **order_data
    )

    if isinstance(result, dict) and "error" in result:
        error_type = result["error"]

        if error_type == "auth":
            return "Please check your credentials and try again."
        elif error_type == "validation":
            return f"Invalid {result['field']}: {result['message']}"
        elif error_type == "not_found":
            return f"{result['resource']} not found. Please check the ID."
        elif error_type == "api":
            return f"Server error ({result['status']}). Please try again later."
        elif error_type == "network":
            return "Network connection issue. Please check your internet."
        else:
            return f"Error: {result['message']}"

    return result  # Success - return the order object

# Example usage
client = PathaoClient(environment="sandbox")

order_data = {
    "store_id": 123,
    "merchant_order_id": "ORDER-001",
    "recipient_name": "John Doe",
    "recipient_phone": "01712345678",
    "recipient_address": "Test Address",
    "recipient_city": 1,
    "recipient_zone": 1,
    "delivery_type": 48,
    "item_type": 2,
    "item_quantity": 1,
    "item_weight": 1.0,
    "amount_to_collect": 100.0
}

result = create_order_safely(client, order_data)
if isinstance(result, str):
    print(f"❌ {result}")  # Error message
else:
    print(f"✅ Order created: {result.consignment_id}")
```

## Retry Logic

```python
import time
from pathao import NetworkError, APIError

def retry_api_call(func, max_retries=3, delay=1, *args, **kwargs):
    """Retry API calls with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)

        except (NetworkError, APIError) as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, re-raise the exception

            wait_time = delay * (2 ** attempt)  # Exponential backoff
            print(f"⏳ Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)

# Usage
try:
    cities = retry_api_call(client.locations.get_cities)
    print(f"✅ Got {len(cities.data)} cities")
except Exception as e:
    print(f"❌ All retry attempts failed: {e}")
```

## Best Practices

1. **Specific Exception Handling**: Catch specific exceptions rather than generic ones
2. **User-Friendly Messages**: Convert technical errors to user-friendly messages
3. **Logging**: Log errors for debugging while showing clean messages to users
4. **Retry Logic**: Implement retry for network and temporary API errors
5. **Graceful Degradation**: Provide fallback behavior when possible
6. **Validation First**: Validate inputs before API calls to avoid server errors
7. **Error Context**: Include relevant context (field names, resource IDs) in error messages
