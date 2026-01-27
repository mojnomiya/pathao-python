# Pathao Python SDK - API Reference

**Version:** 0.1.0
**Last Updated:** January 2026
**Status:** Complete Implementation ✅

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Authentication](#authentication)
5. [API Reference](#api-reference)
   - [Client](#client)
   - [Store Management](#store-management)
   - [Order Management](#order-management)
   - [Location Services](#location-services)
   - [Price Calculation](#price-calculation)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Examples](#examples)

---

## Overview

The Pathao Python SDK provides a clean, Pythonic interface to the Pathao Courier Merchant API. It handles authentication, request/response serialization, error handling, and provides convenient methods for all supported operations.

### Features ✅

- ✅ OAuth 2.0 authentication with automatic token refresh
- ✅ Type hints throughout the codebase
- ✅ Comprehensive input validation
- ✅ Detailed error messages with custom exception hierarchy
- ✅ Support for both Sandbox and Production environments
- ✅ Batch operations support
- ✅ Exponential backoff retry logic
- ✅ Secure logging with sensitive data masking
- ✅ 97% test coverage with 196 unit tests

---

## Installation

### Via pip

```bash
pip install pathao
```

### From source

```bash
git clone https://github.com/yourusername/pathao-python.git
cd pathao-python
pip install -e .
```

### Requirements

- Python 3.8 or higher
- `requests>=2.28.0`
- `python-dotenv>=0.21.0`

---

## Quick Start

### Basic Usage

```python
from pathao import PathaoClient

# Initialize the client
client = PathaoClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_email",
    password="your_password",
    environment="sandbox"  # Use "production" for live
)

# Create an order
order = client.orders.create(
    store_id=1,
    recipient_name="John Doe",
    recipient_phone="01712345678",
    recipient_address="House 123, Road 4, Dhaka",
    delivery_type=48,  # Normal delivery
    item_type=2,  # Parcel
    item_quantity=1,
    item_weight=0.5,
    amount_to_collect=0
)

print(f"Order created: {order.consignment_id}")
```

### Using Environment Variables

Create a `.env` file:

```
PATHAO_CLIENT_ID=your_client_id
PATHAO_CLIENT_SECRET=your_client_secret
PATHAO_USERNAME=your_email
PATHAO_PASSWORD=your_password
PATHAO_ENVIRONMENT=sandbox
```

Then initialize without parameters:

```python
from pathao import PathaoClient

client = PathaoClient()  # Reads from .env
```

---

## Authentication

### PathaoClient Class

```python
class PathaoClient:
    """
    Main client class for Pathao Courier API interactions.

    Handles authentication, token management, and delegates
    operations to specific modules.
    """
```

#### Constructor

```python
def __init__(
    self,
    client_id: str = None,
    client_secret: str = None,
    username: str = None,
    password: str = None,
    environment: str = "sandbox",
    timeout: int = 30,
    max_retries: int = 3,
    retry_backoff: float = 0.3
) -> None:
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client_id` | str | No | From .env | OAuth client ID from Pathao |
| `client_secret` | str | No | From .env | OAuth client secret from Pathao |
| `username` | str | No | From .env | Email registered with Pathao |
| `password` | str | No | From .env | Account password |
| `environment` | str | No | "sandbox" | "sandbox" or "production" |
| `timeout` | int | No | 30 | Request timeout in seconds |
| `max_retries` | int | No | 3 | Max retry attempts for failed requests |
| `retry_backoff` | float | No | 0.3 | Backoff factor for exponential backoff |

**Example:**

```python
client = PathaoClient(
    client_id="7N1aMJQbWm",
    client_secret="wRcaibZkUdSNz2EI9ZyuXLlNrnAv0TdPUPXMnD39",
    username="test@pathao.com",
    password="lovePathao",
    environment="sandbox"
)
```

#### Methods

##### `get_access_token() -> str`

Manually retrieve the current access token. Token is automatically refreshed if expired.

**Returns:** Current valid access token string

**Example:**

```python
token = client.get_access_token()
print(f"Current token: {token}")
```

##### `refresh_token() -> None`

Manually refresh the access token.

**Raises:** `AuthenticationError` if refresh fails

**Example:**

```python
try:
    client.refresh_token()
    print("Token refreshed successfully")
except AuthenticationError as e:
    print(f"Token refresh failed: {e}")
```

##### `is_token_valid() -> bool`

Check if current token is valid and not expired.

**Returns:** True if token is valid, False otherwise

**Example:**

```python
if client.is_token_valid():
    print("Token is still valid")
else:
    print("Token needs refresh")
```

---

## API Reference

### Store Management

#### StoreModule

Module for managing merchant stores.

**Access via:** `client.stores`

#### Methods

##### `create(name: str, contact_name: str, contact_number: str, address: str, city_id: int, zone_id: int, area_id: int, secondary_contact: str = None, otp_number: str = None) -> Store`

Create a new store.

**Parameters:**

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `name` | str | Yes | Length 3-50 | Store name |
| `contact_name` | str | Yes | Length 3-50 | Contact person name |
| `contact_number` | str | Yes | Length 11 | Phone number |
| `address` | str | Yes | Length 15-120 | Full address |
| `city_id` | int | Yes | Valid city_id | City identifier |
| `zone_id` | int | Yes | Valid zone_id | Zone identifier |
| `area_id` | int | Yes | Valid area_id | Area identifier |
| `secondary_contact` | str | No | Length 11 | Secondary phone number |
| `otp_number` | str | No | Length 11 | OTP delivery number |

**Returns:** `Store` object

**Raises:**
- `ValidationError` - Invalid parameters
- `APIError` - API request failed

**Example:**

```python
store = client.stores.create(
    name="My Store",
    contact_name="Store Manager",
    contact_number="01712345678",
    address="House 123, Road 4, Dhaka-1230, Bangladesh",
    city_id=1,
    zone_id=298,
    area_id=37
)

print(f"Store created: {store.name}")
print("Note: Store requires 1 hour for approval")
```

##### `list(page: int = 1, per_page: int = 100) -> StoreList`

Get list of merchant stores.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | int | No | 1 | Page number |
| `per_page` | int | No | 100 | Items per page (max 1000) |

**Returns:** `StoreList` object containing list of stores with pagination info

**Raises:** `APIError` - API request failed

**Example:**

```python
stores = client.stores.list(page=1, per_page=10)

print(f"Total stores: {stores.total}")
print(f"Current page: {stores.current_page}")

for store in stores.data:
    print(f"Store: {store.name} (ID: {store.store_id})")
```

##### `get(store_id: int) -> Store`

Get details of a specific store.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `store_id` | int | Yes | Store identifier |

**Returns:** `Store` object

**Raises:**
- `NotFoundError` - Store not found
- `APIError` - API request failed

**Example:**

```python
store = client.stores.get(store_id=123)
print(f"Store: {store.name}")
print(f"Address: {store.address}")
print(f"Active: {store.is_active}")
```

---

### Order Management

#### OrderModule

Module for managing orders and shipments.

**Access via:** `client.orders`

#### Methods

##### `create(store_id: int, recipient_name: str, recipient_phone: str, recipient_address: str, delivery_type: int, item_type: int, item_quantity: int, item_weight: float, amount_to_collect: int = 0, merchant_order_id: str = None, item_description: str = None, special_instruction: str = None, recipient_secondary_phone: str = None, recipient_city: int = None, recipient_zone: int = None, recipient_area: int = None) -> Order`

Create a single order.

**Parameters:**

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `store_id` | int | Yes | Valid store | Source store ID |
| `recipient_name` | str | Yes | Length 3-100 | Recipient name |
| `recipient_phone` | str | Yes | Length 11 | Recipient phone |
| `recipient_address` | str | Yes | Length 10-220 | Delivery address |
| `delivery_type` | int | Yes | 48 or 12 | 48=Normal, 12=OnDemand |
| `item_type` | int | Yes | 1 or 2 | 1=Document, 2=Parcel |
| `item_quantity` | int | Yes | >= 1 | Number of items |
| `item_weight` | float | Yes | 0.5-10 | Weight in kg |
| `amount_to_collect` | int | No | >= 0 | COD amount (0 for prepaid) |
| `merchant_order_id` | str | No | - | Your order tracking ID |
| `item_description` | str | No | - | Item description |
| `special_instruction` | str | No | - | Delivery instructions |
| `recipient_secondary_phone` | str | No | Length 11 | Secondary contact |
| `recipient_city` | int | No | - | Auto-detected if omitted |
| `recipient_zone` | int | No | - | Auto-detected if omitted |
| `recipient_area` | int | No | - | Auto-detected if omitted |

**Returns:** `Order` object

**Raises:**
- `ValidationError` - Invalid parameters
- `APIError` - API request failed

**Example:**

```python
order = client.orders.create(
    store_id=1,
    merchant_order_id="ORD-2024-001",
    recipient_name="John Doe",
    recipient_phone="01712345678",
    recipient_address="House 123, Road 4, Dhaka-1230",
    delivery_type=48,  # Normal delivery
    item_type=2,       # Parcel
    item_quantity=1,
    item_weight=0.5,
    item_description="T-Shirt",
    special_instruction="Leave with neighbor if not home",
    amount_to_collect=500  # COD amount
)

print(f"Order created: {order.consignment_id}")
print(f"Status: {order.order_status}")
print(f"Delivery fee: {order.delivery_fee} Taka")
```

##### `create_bulk(orders: List[Dict]) -> BulkOrderResponse`

Create multiple orders in a single request.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orders` | List[Dict] | Yes | List of order dictionaries (see create for fields) |

**Returns:** `BulkOrderResponse` object

**Raises:**
- `ValidationError` - Invalid parameters
- `APIError` - API request failed

**Example:**

```python
orders = [
    {
        "store_id": 1,
        "merchant_order_id": "ORD-001",
        "recipient_name": "Customer 1",
        "recipient_phone": "01712345678",
        "recipient_address": "Address 1, Dhaka",
        "delivery_type": 48,
        "item_type": 2,
        "item_quantity": 1,
        "item_weight": 0.5,
        "amount_to_collect": 500
    },
    {
        "store_id": 1,
        "merchant_order_id": "ORD-002",
        "recipient_name": "Customer 2",
        "recipient_phone": "01512345678",
        "recipient_address": "Address 2, Chittagong",
        "delivery_type": 48,
        "item_type": 2,
        "item_quantity": 2,
        "item_weight": 1.0,
        "amount_to_collect": 1000
    }
]

response = client.orders.create_bulk(orders)
print(f"Bulk order submitted for processing")
print(f"Status code: {response.code}")
```

##### `get_info(consignment_id: str) -> OrderInfo`

Get current information about an order.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `consignment_id` | str | Yes | Order consignment ID |

**Returns:** `OrderInfo` object

**Raises:**
- `NotFoundError` - Order not found
- `APIError` - API request failed

**Example:**

```python
order_info = client.orders.get_info("PATHAO_CONSIGNMENT_ID")

print(f"Status: {order_info.order_status}")
print(f"Last updated: {order_info.updated_at}")
print(f"Invoice ID: {order_info.invoice_id}")
```

---

### Location Services

#### LocationModule

Module for retrieving location and service area information.

**Access via:** `client.locations`

#### Methods

##### `get_cities() -> CityList`

Get list of all available cities.

**Returns:** `CityList` object containing list of cities

**Raises:** `APIError` - API request failed

**Example:**

```python
cities = client.locations.get_cities()

print(f"Total cities: {len(cities.data)}")
for city in cities.data:
    print(f"{city.city_name} (ID: {city.city_id})")
```

##### `get_zones(city_id: int) -> ZoneList`

Get list of zones within a city.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city_id` | int | Yes | City identifier |

**Returns:** `ZoneList` object containing list of zones

**Raises:**
- `ValidationError` - Invalid city_id
- `APIError` - API request failed

**Example:**

```python
zones = client.locations.get_zones(city_id=1)

print(f"Zones in Dhaka: {len(zones.data)}")
for zone in zones.data:
    print(f"{zone.zone_name} (ID: {zone.zone_id})")
```

##### `get_areas(zone_id: int) -> AreaList`

Get list of areas within a zone.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `zone_id` | int | Yes | Zone identifier |

**Returns:** `AreaList` object containing list of areas

**Raises:**
- `ValidationError` - Invalid zone_id
- `APIError` - API request failed

**Example:**

```python
areas = client.locations.get_areas(zone_id=298)

for area in areas.data:
    print(f"Area: {area.area_name}")
    print(f"  Home delivery: {area.home_delivery_available}")
    print(f"  Pickup available: {area.pickup_available}")
```

##### `get_city_by_name(name: str) -> City`

Get city by name (case-insensitive).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | str | Yes | City name |

**Returns:** `City` object

**Raises:** `NotFoundError` - City not found

**Example:**

```python
city = client.locations.get_city_by_name("Dhaka")
print(f"Dhaka city ID: {city.city_id}")
```

---

### Price Calculation

#### PriceModule

Module for calculating delivery prices.

**Access via:** `client.prices`

#### Methods

##### `calculate(store_id: int, item_type: int, delivery_type: int, item_weight: float, recipient_city: int, recipient_zone: int) -> PriceDetails`

Calculate delivery price for given parameters.

**Parameters:**

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `store_id` | int | Yes | Valid store | Source store ID |
| `item_type` | int | Yes | 1 or 2 | 1=Document, 2=Parcel |
| `delivery_type` | int | Yes | 48 or 12 | 48=Normal, 12=OnDemand |
| `item_weight` | float | Yes | 0.5-10 | Weight in kg |
| `recipient_city` | int | Yes | Valid city | Destination city ID |
| `recipient_zone` | int | Yes | Valid zone | Destination zone ID |

**Returns:** `PriceDetails` object

**Raises:**
- `ValidationError` - Invalid parameters
- `APIError` - API request failed

**Example:**

```python
price = client.prices.calculate(
    store_id=1,
    item_type=2,        # Parcel
    delivery_type=48,   # Normal
    item_weight=0.5,
    recipient_city=1,   # Dhaka
    recipient_zone=298  # 60 feet
)

print(f"Base price: {price.price} Taka")
print(f"Discount: {price.discount} Taka")
print(f"Final price: {price.final_price} Taka")
print(f"COD enabled: {price.cod_enabled}")
if price.cod_enabled:
    print(f"COD charge: {price.cod_percentage * 100}%")
```

---

## Data Models

### Authentication Models

#### AuthToken

```python
@dataclass
class AuthToken:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    created_at: datetime

    def is_expired(self) -> bool:
        """Check if token has expired"""

    def will_expire_soon(self, seconds: int = 300) -> bool:
        """Check if token will expire in N seconds"""
```

### Store Models

#### Store

```python
@dataclass
class Store:
    store_id: int
    store_name: str
    store_address: str
    is_active: bool
    city_id: int
    zone_id: int
    hub_id: int
    is_default_store: bool
    is_default_return_store: bool
```

#### StoreList

```python
@dataclass
class StoreList:
    data: List[Store]
    total: int
    current_page: int
    per_page: int
    last_page: int
```

### Order Models

#### Order

```python
@dataclass
class Order:
    consignment_id: str
    merchant_order_id: str
    order_status: str
    delivery_fee: float
    created_at: datetime
    updated_at: datetime
```

#### OrderInfo

```python
@dataclass
class OrderInfo:
    consignment_id: str
    merchant_order_id: str
    order_status: str
    order_status_slug: str
    updated_at: str
    invoice_id: str = None
```

### Location Models

#### City

```python
@dataclass
class City:
    city_id: int
    city_name: str
```

#### Zone

```python
@dataclass
class Zone:
    zone_id: int
    zone_name: str
```

#### Area

```python
@dataclass
class Area:
    area_id: int
    area_name: str
    home_delivery_available: bool
    pickup_available: bool
```

### Price Models

#### PriceDetails

```python
@dataclass
class PriceDetails:
    price: float
    discount: float
    promo_discount: float
    plan_id: int
    cod_enabled: bool
    cod_percentage: float
    additional_charge: float
    final_price: float
```

---

## Error Handling

### Exception Hierarchy

```
PathaoException (base)
├── AuthenticationError
├── ValidationError
├── NotFoundError
├── APIError
├── NetworkError
└── ConfigurationError
```

### Exception Classes

#### PathaoException

Base exception for all Pathao SDK errors.

```python
try:
    # SDK operation
except PathaoException as e:
    print(f"Pathao error: {e}")
```

#### AuthenticationError

Raised when authentication fails or token refresh fails.

```python
from pathao.exceptions import AuthenticationError

try:
    client = PathaoClient(
        client_id="invalid",
        client_secret="invalid",
        username="invalid",
        password="invalid"
    )
    client.refresh_token()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

#### ValidationError

Raised when input validation fails.

```python
from pathao.exceptions import ValidationError

try:
    order = client.orders.create(
        store_id=1,
        recipient_name="Jo",  # Too short (min 3)
        # ... other params
    )
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Field: {e.field}")
```

#### NotFoundError

Raised when requested resource is not found.

```python
from pathao.exceptions import NotFoundError

try:
    store = client.stores.get(store_id=9999)
except NotFoundError as e:
    print(f"Store not found: {e}")
```

#### APIError

Raised for general API errors.

```python
from pathao.exceptions import APIError

try:
    order = client.orders.create(...)
except APIError as e:
    print(f"API error code: {e.status_code}")
    print(f"Error message: {e.message}")
```

#### NetworkError

Raised for network-related failures.

```python
from pathao.exceptions import NetworkError

try:
    cities = client.locations.get_cities()
except NetworkError as e:
    print(f"Network error: {e}")
    print(f"Retry after: {e.retry_after} seconds")
```

---

## Examples

### Example 1: Complete Order Creation Workflow

```python
from pathao import PathaoClient
from pathao.exceptions import PathaoException

# Initialize
client = PathaoClient(
    client_id="your_id",
    client_secret="your_secret",
    username="your_email",
    password="your_password"
)

try:
    # Get available cities
    cities = client.locations.get_cities()
    dhaka = next(c for c in cities.data if c.city_name == "Dhaka")

    # Get zones in Dhaka
    zones = client.locations.get_zones(city_id=dhaka.city_id)
    first_zone = zones.data[0]

    # Get areas in zone
    areas = client.locations.get_areas(zone_id=first_zone.zone_id)
    first_area = areas.data[0]

    # Calculate price
    price = client.prices.calculate(
        store_id=1,
        item_type=2,
        delivery_type=48,
        item_weight=0.5,
        recipient_city=dhaka.city_id,
        recipient_zone=first_zone.zone_id
    )

    print(f"Delivery cost: {price.final_price} Taka")

    # Create order
    order = client.orders.create(
        store_id=1,
        merchant_order_id="ORD-2024-001",
        recipient_name="John Doe",
        recipient_phone="01712345678",
        recipient_address="House 123, Road 4, Dhaka",
        recipient_city=dhaka.city_id,
        recipient_zone=first_zone.zone_id,
        recipient_area=first_area.area_id,
        delivery_type=48,
        item_type=2,
        item_quantity=1,
        item_weight=0.5,
        amount_to_collect=1000
    )

    print(f"✓ Order created successfully!")
    print(f"  Consignment ID: {order.consignment_id}")
    print(f"  Status: {order.order_status}")
    print(f"  Fee: {order.delivery_fee} Taka")

except PathaoException as e:
    print(f"✗ Error: {e}")
```

### Example 2: Bulk Order Creation

```python
from pathao import PathaoClient

client = PathaoClient()

orders_data = [
    {
        "store_id": 1,
        "merchant_order_id": f"BULK-{i:04d}",
        "recipient_name": f"Customer {i}",
        "recipient_phone": f"0171234567{i % 10}",
        "recipient_address": f"Address {i}, Dhaka",
        "delivery_type": 48,
        "item_type": 2,
        "item_quantity": 1,
        "item_weight": 0.5,
        "amount_to_collect": 500
    }
    for i in range(1, 11)
]

response = client.orders.create_bulk(orders_data)
print(f"Bulk order submitted: {response.code}")
```

### Example 3: Error Handling

```python
from pathao import PathaoClient
from pathao.exceptions import (
    ValidationError,
    NotFoundError,
    NetworkError,
    PathaoException
)

client = PathaoClient()

try:
    # Attempt to create order with invalid data
    order = client.orders.create(
        store_id=1,
        recipient_name="Jo",  # Too short
        recipient_phone="123",  # Too short
        recipient_address="123 Street",
        delivery_type=999,  # Invalid type
        item_type=5,  # Invalid type
        item_quantity=-1,  # Invalid quantity
        item_weight=0.2,  # Below minimum
        amount_to_collect=0
    )

except ValidationError as e:
    print(f"Validation Error:")
    print(f"  Field: {e.field}")
    print(f"  Message: {e.message}")

except NotFoundError as e:
    print(f"Resource not found: {e}")

except NetworkError as e:
    print(f"Network error: {e}")
    print(f"Retry in {e.retry_after}s")

except PathaoException as e:
    print(f"Pathao error: {e}")
```

---

## Additional Resources

- [GitHub Repository](https://github.com/yourusername/pathao-python)
- [PyPI Package](https://pypi.org/project/pathao/)
- [Official Pathao API Documentation](https://pathao.com/api-docs)
- [Issue Tracker](https://github.com/yourusername/pathao-python/issues)

---

**Documentation Status:** ✅ Complete - Reflects current implementation
**Last Updated:** January 2026
**SDK Version:** 0.1.0
