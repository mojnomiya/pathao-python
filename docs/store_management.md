# Store Management

## Overview

Stores are pickup locations for your orders. You need at least one store to create orders.

## Create Store

```python
from pathao import PathaoClient

client = PathaoClient(environment="sandbox")

# Get location data first
cities = client.locations.get_cities()
dhaka = next(c for c in cities.data if c.city_name.lower() == "dhaka")

zones = client.locations.get_zones(dhaka.city_id)
zone = zones.data[0]

areas = client.locations.get_areas(zone.zone_id)
area = areas.data[0]

# Create store
store = client.stores.create(
    store_name="My Store",
    contact_name="John Doe",
    contact_number="01712345678",
    address="123 Main Street, Dhanmondi, Dhaka",
    city_id=dhaka.city_id,
    zone_id=zone.zone_id,
    area_id=area.area_id
)

print(f"Store created with ID: {store.store_id}")
```

## List Stores

```python
# List all stores (with pagination)
stores = client.stores.list(page=1, per_page=10)

print(f"Total stores: {stores.total}")
for store in stores.data:
    print(f"- {store.store_name} (ID: {store.store_id})")
```

## Get Store Details

```python
# Get specific store
store = client.stores.get(store_id=123)

print(f"Store: {store.store_name}")
print(f"Address: {store.store_address}")
print(f"Active: {store.is_active}")
```

## Store Model

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

## Validation Rules

- **store_name**: 3-50 characters
- **contact_name**: 3-50 characters
- **contact_number**: Exactly 11 digits (01XXXXXXXXX)
- **address**: 15-120 characters
- **city_id, zone_id, area_id**: Must be positive integers

## Error Handling

```python
from pathao import ValidationError, NotFoundError

try:
    store = client.stores.create(
        store_name="Test Store",
        contact_name="John Doe",
        contact_number="123",  # Invalid - too short
        address="Test Address",
        city_id=1,
        zone_id=1,
        area_id=1
    )
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    store = client.stores.get(999999)  # Non-existent store
except NotFoundError as e:
    print(f"Store not found: {e}")
```

## Complete Example

```python
from pathao import PathaoClient, ValidationError, NotFoundError

def setup_store(client):
    """Create a store if none exists."""
    try:
        # Check existing stores
        stores = client.stores.list()
        if stores.data:
            print(f"Using existing store: {stores.data[0].store_name}")
            return stores.data[0]

        # Get location data
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if "dhaka" in c.city_name.lower()), None)

        if not dhaka:
            raise ValueError("Dhaka city not found")

        zones = client.locations.get_zones(dhaka.city_id)
        areas = client.locations.get_areas(zones.data[0].zone_id)

        # Create new store
        store = client.stores.create(
            store_name="My Business Store",
            contact_name="Store Manager",
            contact_number="01712345678",
            address="123 Business Street, Dhanmondi, Dhaka",
            city_id=dhaka.city_id,
            zone_id=zones.data[0].zone_id,
            area_id=areas.data[0].area_id
        )

        print(f" Store created: {store.store_name} (ID: {store.store_id})")
        return store

    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error creating store: {e}")
        return None

# Usage
client = PathaoClient(environment="sandbox")
store = setup_store(client)
```
