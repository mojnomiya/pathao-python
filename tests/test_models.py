"""Tests for Pathao SDK models."""

from datetime import datetime, timedelta
import pytest
from pathao.models import (
    AuthToken,
    Store,
    StoreList,
    Order,
    OrderInfo,
    BulkOrderResponse,
    City,
    CityList,
    Zone,
    ZoneList,
    Area,
    AreaList,
    PriceDetails,
)


class TestAuthToken:
    """Test AuthToken model."""

    def test_auth_token_creation(self):
        """Test AuthToken creation."""
        created_at = datetime.now()
        token = AuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh_token",
            created_at=created_at,
        )

        assert token.access_token == "test_token"
        assert token.token_type == "Bearer"
        assert token.expires_in == 3600
        assert token.refresh_token == "refresh_token"
        assert token.created_at == created_at

    def test_is_expired_false(self):
        """Test token is not expired."""
        token = AuthToken(
            access_token="test",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now(),
        )
        assert not token.is_expired()

    def test_is_expired_true(self):
        """Test token is expired."""
        token = AuthToken(
            access_token="test",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now() - timedelta(hours=2),
        )
        assert token.is_expired()

    def test_will_expire_soon_false(self):
        """Test token will not expire soon."""
        token = AuthToken(
            access_token="test",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now(),
        )
        assert not token.will_expire_soon(300)

    def test_will_expire_soon_true(self):
        """Test token will expire soon."""
        token = AuthToken(
            access_token="test",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now() - timedelta(minutes=58),
        )
        assert token.will_expire_soon(300)


class TestStore:
    """Test Store model."""

    def test_store_creation(self):
        """Test Store creation."""
        store = Store(
            store_id=1,
            store_name="Test Store",
            store_address="Test Address",
            is_active=True,
            city_id=1,
            zone_id=298,
            hub_id=1,
            is_default_store=True,
            is_default_return_store=False,
        )

        assert store.store_id == 1
        assert store.store_name == "Test Store"
        assert store.is_active is True


class TestStoreList:
    """Test StoreList model."""

    def test_store_list_creation(self):
        """Test StoreList creation."""
        stores = [
            Store(1, "Store 1", "Address 1", True, 1, 298, 1, True, False),
            Store(2, "Store 2", "Address 2", True, 1, 298, 1, False, False),
        ]

        store_list = StoreList(
            data=stores, total=2, current_page=1, per_page=10, last_page=1
        )

        assert len(store_list.data) == 2
        assert store_list.total == 2
        assert store_list.current_page == 1


class TestOrder:
    """Test Order model."""

    def test_order_creation(self):
        """Test Order creation."""
        created_at = datetime.now()
        updated_at = datetime.now()

        order = Order(
            consignment_id="PATHAO123",
            merchant_order_id="ORD001",
            order_status="Pending",
            delivery_fee=60.0,
            created_at=created_at,
            updated_at=updated_at,
        )

        assert order.consignment_id == "PATHAO123"
        assert order.merchant_order_id == "ORD001"
        assert order.delivery_fee == 60.0


class TestOrderInfo:
    """Test OrderInfo model."""

    def test_order_info_creation(self):
        """Test OrderInfo creation."""
        order_info = OrderInfo(
            consignment_id="PATHAO123",
            merchant_order_id="ORD001",
            order_status="Delivered",
            order_status_slug="delivered",
            updated_at="2024-01-01 12:00:00",
            invoice_id="INV001",
        )

        assert order_info.consignment_id == "PATHAO123"
        assert order_info.invoice_id == "INV001"

    def test_order_info_without_invoice(self):
        """Test OrderInfo creation without invoice ID."""
        order_info = OrderInfo(
            consignment_id="PATHAO123",
            merchant_order_id="ORD001",
            order_status="Pending",
            order_status_slug="pending",
            updated_at="2024-01-01 12:00:00",
        )

        assert order_info.invoice_id is None


class TestBulkOrderResponse:
    """Test BulkOrderResponse model."""

    def test_bulk_order_response(self):
        """Test BulkOrderResponse creation."""
        response = BulkOrderResponse(
            code=202,
            message="Orders submitted for processing",
            data={"batch_id": "BATCH001"},
        )

        assert response.code == 202
        assert response.message == "Orders submitted for processing"
        assert response.data["batch_id"] == "BATCH001"


class TestLocationModels:
    """Test location models."""

    def test_city_creation(self):
        """Test City creation."""
        city = City(city_id=1, city_name="Dhaka")
        assert city.city_id == 1
        assert city.city_name == "Dhaka"

    def test_city_list_creation(self):
        """Test CityList creation."""
        cities = [City(1, "Dhaka"), City(2, "Chittagong")]
        city_list = CityList(data=cities)
        assert len(city_list.data) == 2

    def test_zone_creation(self):
        """Test Zone creation."""
        zone = Zone(zone_id=298, zone_name="60 feet")
        assert zone.zone_id == 298
        assert zone.zone_name == "60 feet"

    def test_area_creation(self):
        """Test Area creation."""
        area = Area(
            area_id=37,
            area_name="Mirpur 1",
            home_delivery_available=True,
            pickup_available=True,
        )
        assert area.area_id == 37
        assert area.home_delivery_available is True


class TestPriceDetails:
    """Test PriceDetails model."""

    def test_price_details_creation(self):
        """Test PriceDetails creation."""
        price = PriceDetails(
            price=60.0,
            discount=0.0,
            promo_discount=0.0,
            plan_id=1,
            cod_enabled=True,
            cod_percentage=0.01,
            additional_charge=0.0,
            final_price=60.0,
        )

        assert price.price == 60.0
        assert price.cod_enabled is True
        assert price.cod_percentage == 0.01
        assert price.final_price == 60.0
