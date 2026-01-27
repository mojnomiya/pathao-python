#!/usr/bin/env python3
"""
Order creation example for Pathao Python SDK.

This example demonstrates:
- Creating a single order
- Order validation
- Order tracking
- Error handling
"""

import os
import uuid
from pathao import PathaoClient, ValidationError, NotFoundError


def get_or_create_store(client):
    """Get existing store or help create one."""
    try:
        stores = client.stores.list()
        if stores.data:
            store = stores.data[0]
            print(f"✅ Using existing store: {store.store_name} (ID: {store.store_id})")
            return store
        else:
            print("❌ No stores found. Please create a store first.")
            print("💡 Use the store management example or create via API")
            return None

    except Exception as e:
        print(f"❌ Error getting stores: {e}")
        return None


def get_location_data(client):
    """Get location data for order creation."""
    try:
        # Get Dhaka city
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if "dhaka" in c.city_name.lower()), None)

        if not dhaka:
            print("❌ Dhaka city not found")
            return None, None

        # Get first zone in Dhaka
        zones = client.locations.get_zones(dhaka.city_id)
        if not zones.data:
            print("❌ No zones found in Dhaka")
            return dhaka.city_id, None

        zone = zones.data[0]
        print(f"✅ Using location: {dhaka.city_name} > {zone.zone_name}")

        return dhaka.city_id, zone.zone_id

    except Exception as e:
        print(f"❌ Error getting location data: {e}")
        return None, None


def create_sample_order(client, store_id, city_id, zone_id):
    """Create a sample order with proper validation."""
    try:
        # Generate unique order ID
        order_id = f"EXAMPLE-{uuid.uuid4().hex[:8].upper()}"

        print(f"\n📦 Creating order: {order_id}")

        order = client.orders.create(
            store_id=store_id,
            merchant_order_id=order_id,
            recipient_name="John Customer",
            recipient_phone="01712345678",
            recipient_address="123 Customer Street, Dhanmondi, Dhaka",
            recipient_city=city_id,
            recipient_zone=zone_id,
            delivery_type=48,  # Normal delivery (48 hours)
            item_type=2,  # Parcel
            item_quantity=1,
            item_weight=1.0,  # 1kg
            amount_to_collect=150.0,  # COD amount
            item_description="Sample product - Electronics",
        )

        print("✅ Order created successfully!")
        print(f"   Consignment ID: {order.consignment_id}")
        print(f"   Merchant Order ID: {order.merchant_order_id}")
        print(f"   Status: {order.order_status}")
        print(f"   Delivery Fee: ৳{order.delivery_fee}")

        return order

    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if hasattr(e, "field"):
            print(f"   Field: {e.field}")
        return None

    except Exception as e:
        print(f"❌ Error creating order: {e}")
        return None


def track_order(client, consignment_id):
    """Track an order by consignment ID."""
    try:
        print(f"\n🔍 Tracking order: {consignment_id}")

        order_info = client.orders.get_info(consignment_id)

        print("✅ Order found:")
        print(f"   Consignment ID: {order_info.consignment_id}")
        print(f"   Merchant Order ID: {order_info.merchant_order_id}")
        print(f"   Status: {order_info.order_status}")
        print(f"   Status Slug: {order_info.order_status_slug}")
        print(f"   Last Updated: {order_info.updated_at}")

        if order_info.invoice_id:
            print(f"   Invoice ID: {order_info.invoice_id}")

        return order_info

    except NotFoundError as e:
        print(f"❌ Order not found: {e}")
        return None

    except Exception as e:
        print(f"❌ Error tracking order: {e}")
        return None


def demonstrate_validation_errors(client, store_id, city_id, zone_id):
    """Demonstrate common validation errors."""
    print("\n🧪 Demonstrating validation errors...")

    # Invalid phone number
    try:
        client.orders.create(
            store_id=store_id,
            merchant_order_id="INVALID-PHONE",
            recipient_name="Test User",
            recipient_phone="123",  # Too short
            recipient_address="Test Address",
            recipient_city=city_id,
            recipient_zone=zone_id,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=1.0,
            amount_to_collect=0,
        )
    except ValidationError as e:
        print(f"✅ Caught phone validation error: {e}")

    # Invalid weight
    try:
        client.orders.create(
            store_id=store_id,
            merchant_order_id="INVALID-WEIGHT",
            recipient_name="Test User",
            recipient_phone="01712345678",
            recipient_address="Test Address",
            recipient_city=city_id,
            recipient_zone=zone_id,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=15.0,  # Too heavy
            amount_to_collect=0,
        )
    except ValidationError as e:
        print(f"✅ Caught weight validation error: {e}")


def main():
    """Order creation example."""
    print("📦 Pathao Python SDK - Order Creation Example")
    print("=" * 55)

    # Initialize client
    try:
        client = PathaoClient(
            client_id=os.getenv("PATHAO_CLIENT_ID", "your_client_id"),
            client_secret=os.getenv("PATHAO_CLIENT_SECRET", "your_client_secret"),
            username=os.getenv("PATHAO_USERNAME", "your_email@example.com"),
            password=os.getenv("PATHAO_PASSWORD", "your_password"),
            environment="sandbox",
        )
        print("✅ Client initialized")

    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    # Get store
    store = get_or_create_store(client)
    if not store:
        return

    # Get location data
    city_id, zone_id = get_location_data(client)
    if not city_id or not zone_id:
        return

    # Create order
    order = create_sample_order(client, store.store_id, city_id, zone_id)
    if not order:
        return

    # Track the order
    track_order(client, order.consignment_id)

    # Demonstrate validation errors
    demonstrate_validation_errors(client, store.store_id, city_id, zone_id)

    print("\n🎉 Order creation example completed!")
    print("\n📚 What you learned:")
    print("   - How to create orders with proper validation")
    print("   - How to track orders by consignment ID")
    print("   - How to handle validation errors")
    print("   - Order status and delivery fee information")


if __name__ == "__main__":
    main()
