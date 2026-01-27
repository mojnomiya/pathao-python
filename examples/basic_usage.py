#!/usr/bin/env python3
"""
Basic usage example for Pathao Python SDK.

This example demonstrates:
- Client initialization
- Authentication
- Basic API calls
- Error handling
"""

import os
from pathao import PathaoClient, AuthenticationError


def main():
    """Basic usage example."""
    print("🚀 Pathao Python SDK - Basic Usage Example")
    print("=" * 50)

    # Initialize client
    try:
        client = PathaoClient(
            client_id=os.getenv("PATHAO_CLIENT_ID", "7N1aMJQbWm"),
            client_secret=os.getenv(
                "PATHAO_CLIENT_SECRET", "wRcaibZkUdSNz2EI9ZyuXLlNrnAv0TdPUPXMnD39"
            ),
            username=os.getenv("PATHAO_USERNAME", "test@pathao.com"),
            password=os.getenv("PATHAO_PASSWORD", "lovePathao"),
            environment="sandbox",  # Use "production" for live
        )
        print(" Client initialized successfully")

    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    # Test authentication
    try:
        token = client.get_access_token()
        print(" Authentication successful")
        print(f"🔑 Token: {token[:20]}...")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Please check your credentials in environment variables:")
        print("   - PATHAO_CLIENT_ID")
        print("   - PATHAO_CLIENT_SECRET")
        print("   - PATHAO_USERNAME")
        print("   - PATHAO_PASSWORD")
        return

    # Get cities
    try:
        print("\n📍 Getting cities...")
        cities = client.locations.get_cities()
        print(f" Found {len(cities.data)} cities")

        for city in cities.data[:5]:  # Show first 5
            print(f"   - {city.city_name} (ID: {city.city_id})")

    except Exception as e:
        print(f"❌ Failed to get cities: {e}")

    # Get stores
    try:
        print("\n🏪 Getting stores...")
        stores = client.stores.list()
        print(f" Found {len(stores.data)} stores")

        for store in stores.data[:3]:  # Show first 3
            print(f"   - {store.store_name} (ID: {store.store_id})")

    except Exception as e:
        print(f"❌ Failed to get stores: {e}")

    # Calculate price (if we have stores and cities)
    try:
        if (
            "stores" in locals()
            and stores.data
            and "cities" in locals()
            and cities.data
        ):
            print("\n💰 Calculating delivery price...")

            # Get zone for first city
            zones = client.locations.get_zones(cities.data[0].city_id)
            if zones.data:
                price = client.prices.calculate(
                    store_id=stores.data[0].store_id,
                    delivery_type=48,  # Normal delivery
                    item_type=2,  # Parcel
                    item_weight=1.0,  # 1kg
                    recipient_city=cities.data[0].city_id,
                    recipient_zone=zones.data[0].zone_id,
                )

                print(" Price calculated:")
                print(f"   Base price: ৳{price.price}")
                print(f"   Final price: ৳{price.final_price}")
                print(f"   COD available: {price.cod_enabled}")

    except Exception as e:
        print(f"❌ Failed to calculate price: {e}")

    print("\n🎉 Basic usage example completed!")
    print("\n📚 Next steps:")
    print("   - Check other examples in the examples/ directory")
    print("   - Read the documentation in docs/")
    print("   - Try creating stores and orders")


if __name__ == "__main__":
    main()
