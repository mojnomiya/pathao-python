# Order Management

## Overview

Orders represent delivery requests. You can create single orders or bulk orders.

## Create Single Order

```python
from pathao import PathaoClient

client = PathaoClient(environment="sandbox")

# Create order
order = client.orders.create(
    store_id=123,
    merchant_order_id="ORDER-001",
    recipient_name="Jane Smith",
    recipient_phone="01987654321",
    recipient_address="456 Customer Street, Gulshan, Dhaka",
    recipient_city=1,  # Dhaka city ID
    recipient_zone=2,  # Gulshan zone ID
    delivery_type=48,  # Normal delivery (48 hours)
    item_type=2,       # Parcel
    item_quantity=1,
    item_weight=0.5,   # kg
    amount_to_collect=150.0,  # COD amount
    item_description="Customer order - electronics"
)

print(f"Order created: {order.consignment_id}")
```

## Create Bulk Orders

```python
# Prepare multiple orders
orders = [
    {
        "store_id": 123,
        "merchant_order_id": "BULK-001",
        "recipient_name": "Alice Johnson",
        "recipient_phone": "01555666777",
        "recipient_address": "789 Test Street, Dhaka",
        "recipient_city": 1,
        "recipient_zone": 1,
        "delivery_type": 48,
        "item_type": 1,  # Document
        "item_quantity": 1,
        "item_weight": 0.3,
        "amount_to_collect": 75.0,
        "item_description": "Document delivery"
    },
    {
        "store_id": 123,
        "merchant_order_id": "BULK-002",
        "recipient_name": "Bob Wilson",
        "recipient_phone": "01444555666",
        "recipient_address": "321 Another Street, Dhaka",
        "recipient_city": 1,
        "recipient_zone": 2,
        "delivery_type": 12,  # On-demand
        "item_type": 2,       # Parcel
        "item_quantity": 2,
        "item_weight": 1.5,
        "amount_to_collect": 200.0,
        "item_description": "Urgent parcel"
    }
]

# Create bulk orders
response = client.orders.create_bulk(orders)
print(f"Bulk order response: {response.message}")
```

## Track Order

```python
# Get order information
order_info = client.orders.get_info("D-12345")

print(f"Order: {order_info.consignment_id}")
print(f"Status: {order_info.order_status}")
print(f"Updated: {order_info.updated_at}")
```

## Order Models

```python
@dataclass
class Order:
    consignment_id: str
    merchant_order_id: str
    order_status: str
    delivery_fee: float
    created_at: datetime
    updated_at: datetime

@dataclass
class OrderInfo:
    consignment_id: str
    merchant_order_id: str
    order_status: str
    order_status_slug: str
    updated_at: str
    invoice_id: Optional[str] = None
```

## Delivery Types

- **12**: On-demand delivery (same day)
- **48**: Normal delivery (within 48 hours)

## Item Types

- **1**: Document
- **2**: Parcel

## Validation Rules

- **merchant_order_id**: Required, unique identifier
- **recipient_name**: 3-100 characters
- **recipient_phone**: Exactly 11 digits
- **recipient_address**: 10-220 characters
- **item_weight**: 0.5-10.0 kg
- **item_quantity**: Positive integer
- **amount_to_collect**: Non-negative number

## Error Handling

```python
from pathao import ValidationError, NotFoundError

try:
    order = client.orders.create(
        store_id=123,
        merchant_order_id="TEST-001",
        recipient_name="Test User",
        recipient_phone="123",  # Invalid - too short
        recipient_address="Test Address",
        recipient_city=1,
        recipient_zone=1,
        delivery_type=48,
        item_type=2,
        item_quantity=1,
        item_weight=0.5,
        amount_to_collect=0
    )
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    order_info = client.orders.get_info("INVALID-ID")
except NotFoundError as e:
    print(f"Order not found: {e}")
```

## Complete Example

```python
from pathao import PathaoClient, ValidationError
import uuid

def create_sample_order(client, store_id):
    """Create a sample order with proper validation."""
    try:
        # Generate unique order ID
        order_id = f"ORDER-{uuid.uuid4().hex[:8].upper()}"

        order = client.orders.create(
            store_id=store_id,
            merchant_order_id=order_id,
            recipient_name="John Customer",
            recipient_phone="01712345678",
            recipient_address="123 Customer Address, Dhanmondi, Dhaka",
            recipient_city=1,  # Dhaka
            recipient_zone=1,  # Dhanmondi
            delivery_type=48,  # Normal delivery
            item_type=2,       # Parcel
            item_quantity=1,
            item_weight=1.0,
            amount_to_collect=100.0,
            item_description="Sample product delivery"
        )

        print(f"✅ Order created: {order.consignment_id}")

        # Track the order
        order_info = client.orders.get_info(order.consignment_id)
        print(f"📦 Status: {order_info.order_status}")

        return order

    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        return None

# Usage
client = PathaoClient(environment="sandbox")
stores = client.stores.list()
if stores.data:
    order = create_sample_order(client, stores.data[0].store_id)
```
