"""Price calculation module for Pathao Python SDK."""

from typing import TYPE_CHECKING

from ..models import PriceDetails
from ..validators import validate_item_type, validate_delivery_type, validate_weight

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from .auth import AuthModule


class PriceModule:
    """Price calculation operations."""

    def __init__(self, http_client: "HTTPClient", auth_module: "AuthModule"):
        """Initialize price module."""
        self.http_client = http_client
        self.auth_module = auth_module

    def calculate(
        self,
        store_id: int,
        item_type: int,
        delivery_type: int,
        item_weight: float,
        recipient_city: int,
        recipient_zone: int,
    ) -> PriceDetails:
        """Calculate delivery price."""
        # Validate inputs
        if not isinstance(store_id, int) or store_id <= 0:
            raise ValueError("store_id must be a positive integer")

        item_type = validate_item_type(item_type)
        delivery_type = validate_delivery_type(delivery_type)
        item_weight = validate_weight(item_weight)

        if not isinstance(recipient_city, int) or recipient_city <= 0:
            raise ValueError("recipient_city must be a positive integer")
        if not isinstance(recipient_zone, int) or recipient_zone <= 0:
            raise ValueError("recipient_zone must be a positive integer")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "store_id": store_id,
            "item_type": item_type,
            "delivery_type": delivery_type,
            "item_weight": item_weight,
            "recipient_city": recipient_city,
            "recipient_zone": recipient_zone,
        }

        # Make API request
        response = self.http_client.post(
            "aladdin/api/v1/merchant/price-plan", headers, data
        )

        # Parse response
        if "data" in response and "data" in response["data"]:
            price_data = response["data"]["data"]
        elif "data" in response:
            price_data = response["data"]
        else:
            price_data = response

        return PriceDetails(
            price=float(price_data["price"]),
            discount=float(price_data["discount"]),
            promo_discount=float(price_data["promo_discount"]),
            plan_id=price_data["plan_id"],
            cod_enabled=price_data["cod_enabled"],
            cod_percentage=float(price_data["cod_percentage"]),
            additional_charge=float(price_data["additional_charge"]),
            final_price=float(price_data["final_price"]),
        )
