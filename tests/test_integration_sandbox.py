"""Comprehensive integration tests for Pathao Python SDK using sandbox credentials."""

import pytest
import os
from pathao import PathaoClient
from pathao.exceptions import ValidationError, NotFoundError


class TestPathaoSandboxIntegration:
    """Integration tests using real sandbox credentials."""

    @pytest.fixture(scope="class")
    def client(self):
        """Create a PathaoClient instance with sandbox credentials."""
        return PathaoClient(
            client_id=os.getenv("PATHAO_CLIENT_ID", "test_client_id"),
            client_secret=os.getenv("PATHAO_CLIENT_SECRET", "test_client_secret"),
            username=os.getenv("PATHAO_USERNAME", "test@example.com"),
            password=os.getenv("PATHAO_PASSWORD", "test_password"),
            environment="sandbox",
        )

    def test_authentication_flow(self, client):
        """Test authentication and token management."""
        # Get access token
        token = client.get_access_token()
        assert token is not None
        assert len(token) > 0

        # Check token validity
        assert client.is_token_valid() is True

        # Test token refresh
        client.refresh_token()
        new_token = client.get_access_token()
        assert new_token is not None

    def test_location_services_workflow(self, client):
        """Test complete location services workflow."""
        # Get all cities
        cities = client.locations.get_cities()
        assert len(cities.data) > 0

        dhaka_city = None
        for city in cities.data:
            if city.city_name.lower() == "dhaka":
                dhaka_city = city
                break

        assert dhaka_city is not None, "Dhaka city should be available"

        # Get zones for Dhaka
        zones = client.locations.get_zones(dhaka_city.city_id)
        assert len(zones.data) > 0

        # Get areas for first zone
        first_zone = zones.data[0]
        areas = client.locations.get_areas(first_zone.zone_id)
        assert len(areas.data) > 0

        # Test city search
        found_city = client.locations.get_city_by_name("dhaka")
        assert found_city is not None
        assert found_city.city_name.lower() == "dhaka"

    def test_store_management_workflow(self, client):
        """Test complete store management workflow."""
        # Get cities and zones for store creation
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if c.city_name.lower() == "dhaka"), None)
        assert dhaka is not None

        zones = client.locations.get_zones(dhaka.city_id)
        zone = zones.data[0]

        areas = client.locations.get_areas(zone.zone_id)
        area = areas.data[0]

        # Create a test store
        store = client.stores.create(
            store_name="Integration Test Store",
            contact_name="John Doe",
            contact_number="01712345678",
            address="123 Test Street, Dhanmondi, Dhaka",
            city_id=dhaka.city_id,
            zone_id=zone.zone_id,
            area_id=area.area_id,
        )

        assert store.store_id > 0
        assert store.store_name == "Integration Test Store"

        # List stores
        store_list = client.stores.list()
        assert len(store_list.data) > 0

        # Get specific store
        retrieved_store = client.stores.get(store.store_id)
        assert retrieved_store.store_id == store.store_id
        assert retrieved_store.store_name == store.store_name

    def test_price_calculation_workflow(self, client):
        """Test price calculation for different scenarios."""
        # Get location data
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if c.city_name.lower() == "dhaka"), None)

        zones = client.locations.get_zones(dhaka.city_id)
        zone = zones.data[0]

        # Get or create a store
        stores = client.stores.list()
        store_id = stores.data[0].store_id if stores.data else 1

        # Test normal delivery pricing
        normal_price = client.prices.calculate(
            store_id=store_id,
            delivery_type=48,  # Normal
            item_type=2,  # Parcel
            item_weight=1.0,
            recipient_city=dhaka.city_id,
            recipient_zone=zone.zone_id,
        )

        assert normal_price.price > 0
        assert normal_price.final_price >= 0
        assert isinstance(normal_price.cod_enabled, bool)

        # Test on-demand delivery pricing
        ondemand_price = client.prices.calculate(
            store_id=store_id,
            delivery_type=12,  # On-demand
            item_type=1,  # Document
            item_weight=0.5,
            recipient_city=dhaka.city_id,
            recipient_zone=zone.zone_id,
        )

        assert ondemand_price.price > 0
        # On-demand should typically be more expensive
        assert ondemand_price.price >= normal_price.price

    def test_order_management_workflow(self, client):
        """Test complete order management workflow."""
        # Get required data
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if c.city_name.lower() == "dhaka"), None)

        zones = client.locations.get_zones(dhaka.city_id)
        zone = zones.data[0]

        stores = client.stores.list()
        store_id = stores.data[0].store_id if stores.data else 1

        # Create a single order
        order = client.orders.create(
            store_id=store_id,
            merchant_order_id=f"INT-TEST-{os.getpid()}",  # Unique order ID
            recipient_name="Jane Smith",
            recipient_phone="01987654321",
            recipient_address="456 Test Road, Gulshan, Dhaka",
            recipient_city=dhaka.city_id,
            recipient_zone=zone.zone_id,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=0.5,
            amount_to_collect=150.0,
            item_description="Test integration order",
        )

        assert order.consignment_id is not None
        assert len(order.consignment_id) > 0
        assert order.order_status is not None

        # Get order information
        order_info = client.orders.get_info(order.consignment_id)
        assert order_info.consignment_id == order.consignment_id
        assert order_info.order_status is not None

        # Test bulk order creation
        bulk_orders = [
            {
                "store_id": store_id,
                "merchant_order_id": f"BULK-1-{os.getpid()}",
                "recipient_name": "Alice Johnson",
                "recipient_phone": "01555666777",
                "recipient_address": "789 Bulk Test St, Dhaka",
                "recipient_city": dhaka.city_id,
                "recipient_zone": zone.zone_id,
                "delivery_type": 48,
                "item_type": 1,
                "item_quantity": 1,
                "item_weight": 0.3,
                "amount_to_collect": 75.0,
                "item_description": "Bulk test order 1",
            },
            {
                "store_id": store_id,
                "merchant_order_id": f"BULK-2-{os.getpid()}",
                "recipient_name": "Bob Wilson",
                "recipient_phone": "01444555666",
                "recipient_address": "321 Another Test Ave, Dhaka",
                "recipient_city": dhaka.city_id,
                "recipient_zone": zone.zone_id,
                "delivery_type": 12,
                "item_type": 2,
                "item_quantity": 2,
                "item_weight": 1.5,
                "amount_to_collect": 200.0,
                "item_description": "Bulk test order 2",
            },
        ]

        bulk_response = client.orders.create_bulk(bulk_orders)
        assert bulk_response.code in [200, 202]  # Success or accepted for processing
        assert bulk_response.message is not None

    def test_validation_errors(self, client):
        """Test validation error handling across modules."""
        # Test invalid phone number
        with pytest.raises(
            ValidationError, match="Phone number must be exactly 11 digits"
        ):
            client.stores.create(
                store_name="Test Store",
                contact_name="John Doe",
                contact_number="123",  # Too short
                address="123 Test Street, Dhaka",
                city_id=1,
                zone_id=1,
                area_id=1,
            )

        # Test invalid weight
        with pytest.raises(ValidationError, match="Weight must be between"):
            client.orders.create(
                store_id=1,
                merchant_order_id="TEST-INVALID",
                recipient_name="Test User",
                recipient_phone="01712345678",
                recipient_address="Test Address, Dhaka",
                recipient_city=1,
                recipient_zone=1,
                delivery_type=48,
                item_type=2,
                item_quantity=1,
                item_weight=15.0,  # Too heavy
                amount_to_collect=0,
            )

        # Test invalid delivery type
        with pytest.raises(ValidationError, match="Delivery type must be"):
            client.prices.calculate(
                store_id=1,
                delivery_type=99,  # Invalid
                item_type=2,
                item_weight=1.0,
                recipient_city=1,
                recipient_zone=1,
            )

    def test_not_found_errors(self, client):
        """Test not found error handling."""
        # Test non-existent store
        with pytest.raises(NotFoundError):
            client.stores.get(999999)

        # Test non-existent order
        with pytest.raises(NotFoundError):
            client.orders.get_info("INVALID-CONSIGNMENT-ID")

        # Test non-existent city for zones
        with pytest.raises(NotFoundError):
            client.locations.get_zones(999999)

    def test_environment_configuration(self):
        """Test environment configuration."""
        # Test sandbox environment
        sandbox_client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test@example.com",
            password="test_password",
            environment="sandbox",
        )
        assert "sandbox" in sandbox_client.http_client.base_url

        # Test production environment
        prod_client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test@example.com",
            password="test_password",
            environment="production",
        )
        assert "api.pathao.com" in prod_client.http_client.base_url

    def test_credential_management(self):
        """Test credential loading from environment variables."""
        # Set environment variables
        os.environ["PATHAO_CLIENT_ID"] = "env_client_id"
        os.environ["PATHAO_CLIENT_SECRET"] = "env_client_secret"
        os.environ["PATHAO_USERNAME"] = "env@example.com"
        os.environ["PATHAO_PASSWORD"] = "env_password"

        try:
            # Create client without parameters (should use env vars)
            env_client = PathaoClient(environment="sandbox")

            # Verify credentials were loaded from environment
            assert env_client.auth.credentials["client_id"] == "env_client_id"
            assert env_client.auth.credentials["username"] == "env@example.com"

        finally:
            # Clean up environment variables
            for key in [
                "PATHAO_CLIENT_ID",
                "PATHAO_CLIENT_SECRET",
                "PATHAO_USERNAME",
                "PATHAO_PASSWORD",
            ]:
                os.environ.pop(key, None)

    def test_concurrent_operations(self, client):
        """Test that multiple operations work correctly in sequence."""
        # This tests that the client maintains state correctly across operations

        # 1. Get locations
        cities = client.locations.get_cities()
        dhaka = next((c for c in cities.data if c.city_name.lower() == "dhaka"), None)

        # 2. Calculate price
        stores = client.stores.list()
        store_id = stores.data[0].store_id if stores.data else 1

        zones = client.locations.get_zones(dhaka.city_id)
        zone = zones.data[0]

        price = client.prices.calculate(
            store_id=store_id,
            delivery_type=48,
            item_type=2,
            item_weight=1.0,
            recipient_city=dhaka.city_id,
            recipient_zone=zone.zone_id,
        )

        # 3. Create order
        order = client.orders.create(
            store_id=store_id,
            merchant_order_id=f"CONCURRENT-{os.getpid()}",
            recipient_name="Concurrent Test",
            recipient_phone="01712345678",
            recipient_address="Concurrent Test Address",
            recipient_city=dhaka.city_id,
            recipient_zone=zone.zone_id,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=1.0,
            amount_to_collect=price.final_price,
        )

        # 4. Get order info
        order_info = client.orders.get_info(order.consignment_id)

        # All operations should succeed
        assert cities is not None
        assert price is not None
        assert order is not None
        assert order_info is not None
        assert order_info.consignment_id == order.consignment_id
