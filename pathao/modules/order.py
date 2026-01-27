"""Order management module for Pathao Python SDK."""

from typing import List, TYPE_CHECKING

from ..exceptions import NotFoundError
from ..models import Order, OrderInfo, BulkOrderResponse
from ..validators import (
    validate_name,
    validate_phone,
    validate_address,
    validate_weight,
    validate_quantity,
    validate_delivery_type,
    validate_item_type,
)

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from .auth import AuthModule


class OrderModule:
    """Order management operations."""

    def __init__(self, http_client: "HTTPClient", auth_module: "AuthModule"):
        """Initialize order module."""
        self.http_client = http_client
        self.auth_module = auth_module

    def create(
        self,
        store_id: int,
        merchant_order_id: str,
        recipient_name: str,
        recipient_phone: str,
        recipient_address: str,
        recipient_city: int,
        recipient_zone: int,
        delivery_type: int,
        item_type: int,
        item_quantity: int,
        item_weight: float,
        amount_to_collect: float,
        item_description: str = "",
    ) -> Order:
        """Create a new order."""
        # Validate inputs
        if not isinstance(store_id, int) or store_id <= 0:
            raise ValueError("store_id must be a positive integer")

        merchant_order_id = merchant_order_id.strip() if merchant_order_id else ""
        if not merchant_order_id:
            raise ValueError("merchant_order_id is required")

        recipient_name = validate_name(recipient_name, min_length=3, max_length=100)
        recipient_phone = validate_phone(recipient_phone, length=11)
        recipient_address = validate_address(
            recipient_address, min_length=10, max_length=220
        )

        if not isinstance(recipient_city, int) or recipient_city <= 0:
            raise ValueError("recipient_city must be a positive integer")
        if not isinstance(recipient_zone, int) or recipient_zone <= 0:
            raise ValueError("recipient_zone must be a positive integer")

        delivery_type = validate_delivery_type(delivery_type)
        item_type = validate_item_type(item_type)
        item_quantity = validate_quantity(item_quantity)
        item_weight = validate_weight(item_weight)

        if amount_to_collect < 0:
            raise ValueError("amount_to_collect must be non-negative")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "store_id": store_id,
            "merchant_order_id": merchant_order_id,
            "recipient_name": recipient_name,
            "recipient_phone": recipient_phone,
            "recipient_address": recipient_address,
            "recipient_city": recipient_city,
            "recipient_zone": recipient_zone,
            "delivery_type": delivery_type,
            "item_type": item_type,
            "item_quantity": item_quantity,
            "item_weight": item_weight,
            "amount_to_collect": amount_to_collect,
            "item_description": item_description,
        }

        # Make API request
        response = self.http_client.post("aladdin/api/v1/orders", headers, data)

        # Parse response
        order_data = response["data"]["data"]
        return Order(
            consignment_id=order_data["consignment_id"],
            merchant_order_id=order_data["merchant_order_id"],
            order_status=order_data["order_status"],
            delivery_fee=float(order_data["delivery_fee"]),
            created_at=order_data["created_at"],
            updated_at=order_data["updated_at"],
        )

    def create_bulk(self, orders: List[dict]) -> BulkOrderResponse:
        """Create multiple orders in bulk."""
        if not orders or not isinstance(orders, list):
            raise ValueError("orders must be a non-empty list")

        # Validate each order
        validated_orders = []
        for i, order in enumerate(orders):
            try:
                # Basic validation - same as create method but without API call
                if not isinstance(order.get("store_id"), int) or order["store_id"] <= 0:
                    raise ValueError("store_id must be a positive integer")

                merchant_order_id = order.get("merchant_order_id", "").strip()
                if not merchant_order_id:
                    raise ValueError("merchant_order_id is required")

                validated_order = {
                    "store_id": order["store_id"],
                    "merchant_order_id": merchant_order_id,
                    "recipient_name": validate_name(order["recipient_name"], 3, 100),
                    "recipient_phone": validate_phone(order["recipient_phone"], 11),
                    "recipient_address": validate_address(
                        order["recipient_address"], 10, 220
                    ),
                    "recipient_city": order["recipient_city"],
                    "recipient_zone": order["recipient_zone"],
                    "delivery_type": validate_delivery_type(order["delivery_type"]),
                    "item_type": validate_item_type(order["item_type"]),
                    "item_quantity": validate_quantity(order["item_quantity"]),
                    "item_weight": validate_weight(order["item_weight"]),
                    "amount_to_collect": float(order.get("amount_to_collect", 0)),
                    "item_description": order.get("item_description", ""),
                }

                if validated_order["amount_to_collect"] < 0:
                    raise ValueError("amount_to_collect must be non-negative")

                validated_orders.append(validated_order)
            except Exception as e:
                raise ValueError(f"Order {i}: {str(e)}")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}
        data = {"orders": validated_orders}

        # Make API request
        response = self.http_client.post("aladdin/api/v1/orders/bulk", headers, data)

        # Parse response (bulk orders return 202 for async processing)
        return BulkOrderResponse(
            code=response.get("code", 202),
            message=response.get("message", "Orders submitted for processing"),
            data=response.get("data"),
        )

    def get_info(self, consignment_id: str) -> OrderInfo:
        """Get order information by consignment ID."""
        if not consignment_id or not isinstance(consignment_id, str):
            raise ValueError("consignment_id is required and must be a string")

        consignment_id = consignment_id.strip()
        if not consignment_id:
            raise ValueError("consignment_id cannot be empty")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}

        try:
            # Make API request
            response = self.http_client.get(
                f"aladdin/api/v1/orders/{consignment_id}", headers
            )

            # Parse response
            order_data = response["data"]
            return OrderInfo(
                consignment_id=order_data["consignment_id"],
                merchant_order_id=order_data["merchant_order_id"],
                order_status=order_data["order_status"],
                order_status_slug=order_data["order_status_slug"],
                updated_at=order_data["updated_at"],
                invoice_id=order_data.get("invoice_id"),
            )
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise NotFoundError("Order", consignment_id)
            raise
