"""Pathao Python SDK - A comprehensive Python SDK for the Pathao Courier Merchant API."""

__version__ = "0.1.0"

# Import main client
from .client import PathaoClient

# Import all exception classes
from .exceptions import (
    PathaoException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
)

# Import all model classes
from .models import (
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

# Define public API
__all__ = [
    # Main client
    "PathaoClient",
    # Exceptions
    "PathaoException",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "APIError",
    "NetworkError",
    "ConfigurationError",
    # Models
    "AuthToken",
    "Store",
    "StoreList",
    "Order",
    "OrderInfo",
    "BulkOrderResponse",
    "City",
    "CityList",
    "Zone",
    "ZoneList",
    "Area",
    "AreaList",
    "PriceDetails",
]