"""Data models for Pathao Python SDK."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AuthToken:
    """Authentication token model."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    created_at: datetime

    def is_expired(self) -> bool:
        """Check if token has expired."""
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed >= self.expires_in

    def will_expire_soon(self, seconds: int = 300) -> bool:
        """Check if token will expire in N seconds."""
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return (elapsed + seconds) >= self.expires_in


@dataclass
class Store:
    """Store model."""

    store_id: int
    store_name: str
    store_address: str
    is_active: bool
    city_id: int
    zone_id: int
    hub_id: int
    is_default_store: bool
    is_default_return_store: bool


@dataclass
class StoreList:
    """Store list with pagination."""

    data: List[Store]
    total: int
    current_page: int
    per_page: int
    last_page: int


@dataclass
class Order:
    """Order response model."""

    consignment_id: str
    merchant_order_id: str
    order_status: str
    delivery_fee: float
    created_at: datetime
    updated_at: datetime


@dataclass
class OrderInfo:
    """Order information model."""

    consignment_id: str
    merchant_order_id: str
    order_status: str
    order_status_slug: str
    updated_at: str
    invoice_id: Optional[str] = None


@dataclass
class BulkOrderResponse:
    """Bulk order response model."""

    code: int
    message: str
    data: Optional[dict] = None


@dataclass
class City:
    """City model."""

    city_id: int
    city_name: str


@dataclass
class CityList:
    """City list model."""

    data: List[City]


@dataclass
class Zone:
    """Zone model."""

    zone_id: int
    zone_name: str


@dataclass
class ZoneList:
    """Zone list model."""

    data: List[Zone]


@dataclass
class Area:
    """Area model."""

    area_id: int
    area_name: str
    home_delivery_available: bool
    pickup_available: bool


@dataclass
class AreaList:
    """Area list model."""

    data: List[Area]


@dataclass
class PriceDetails:
    """Price calculation model."""

    price: float
    discount: float
    promo_discount: float
    plan_id: int
    cod_enabled: bool
    cod_percentage: float
    additional_charge: float
    final_price: float
