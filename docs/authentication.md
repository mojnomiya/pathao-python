# Authentication Guide

## Overview

The Pathao Python SDK uses OAuth 2.0 authentication with automatic token management. You need merchant credentials from Pathao to use the API.

## Getting Credentials

1. Contact Pathao to get merchant API access
2. You'll receive:
   - Client ID
   - Client Secret
   - Username (email)
   - Password

## Authentication Methods

### Method 1: Direct Parameters

```python
from pathao import PathaoClient

client = PathaoClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_email@example.com",
    password="your_password",
    environment="sandbox"  # or "production"
)
```

### Method 2: Environment Variables

```python
import os
from pathao import PathaoClient

# Set environment variables first
os.environ["PATHAO_CLIENT_ID"] = "your_client_id"
os.environ["PATHAO_CLIENT_SECRET"] = "your_client_secret"
os.environ["PATHAO_USERNAME"] = "your_email@example.com"
os.environ["PATHAO_PASSWORD"] = "your_password"

# Create client (will auto-load from environment)
client = PathaoClient(environment="sandbox")
```

### Method 3: .env File

Create `.env` file:
```env
PATHAO_CLIENT_ID=your_client_id
PATHAO_CLIENT_SECRET=your_client_secret
PATHAO_USERNAME=your_email@example.com
PATHAO_PASSWORD=your_password
```

```python
from pathao import PathaoClient

# Will automatically load from .env file
client = PathaoClient(environment="sandbox")
```

## Token Management

The SDK automatically handles token lifecycle:

```python
# Get current access token
token = client.get_access_token()

# Check if token is valid
is_valid = client.is_token_valid()

# Manually refresh token (usually not needed)
client.refresh_token()
```

## Environments

### Sandbox Environment
- For testing and development
- Use `environment="sandbox"`
- API Base URL: `https://courier-api-sandbox.pathao.com`

### Production Environment
- For live operations
- Use `environment="production"`
- API Base URL: `https://api.pathao.com`

## Error Handling

```python
from pathao import PathaoClient, AuthenticationError

try:
    client = PathaoClient(
        client_id="invalid_id",
        client_secret="invalid_secret",
        username="invalid@email.com",
        password="invalid_password",
        environment="sandbox"
    )

    # This will trigger authentication
    token = client.get_access_token()

except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## Best Practices

1. **Use Environment Variables**: Don't hardcode credentials in your code
2. **Use Sandbox First**: Test with sandbox before production
3. **Handle Auth Errors**: Always wrap API calls in try-catch blocks
4. **Token Caching**: The SDK automatically caches and refreshes tokens
5. **Secure Storage**: Store credentials securely in production

## Example: Complete Setup

```python
import os
from pathao import PathaoClient, AuthenticationError

def create_pathao_client():
    """Create and authenticate Pathao client."""
    try:
        client = PathaoClient(
            client_id=os.getenv("PATHAO_CLIENT_ID"),
            client_secret=os.getenv("PATHAO_CLIENT_SECRET"),
            username=os.getenv("PATHAO_USERNAME"),
            password=os.getenv("PATHAO_PASSWORD"),
            environment=os.getenv("PATHAO_ENV", "sandbox")
        )

        # Test authentication
        token = client.get_access_token()
        print("✅ Authentication successful")

        return client

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return None

# Usage
client = create_pathao_client()
if client:
    # Use client for API calls
    cities = client.locations.get_cities()
    print(f"Found {len(cities.data)} cities")
```
