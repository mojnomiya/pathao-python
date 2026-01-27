"""Mock API responses for Pathao Python SDK tests."""

# Authentication responses
AUTH_SUCCESS_RESPONSE = {
    "access_token": "mock_access_token_12345",
    "refresh_token": "mock_refresh_token_67890",
    "expires_in": 3600,
    "token_type": "Bearer",
}

AUTH_REFRESH_RESPONSE = {
    "access_token": "new_mock_access_token_12345",
    "refresh_token": "new_mock_refresh_token_67890",
    "expires_in": 3600,
    "token_type": "Bearer",
}

AUTH_ERROR_RESPONSE = {
    "error": "invalid_credentials",
    "error_description": "Invalid username or password",
}

# Store responses
STORE_CREATE_SUCCESS = {
    "type": "success",
    "data": {
        "store_id": 123,
        "name": "Test Store",
        "contact_name": "John Doe",
        "contact_number": "01712345678",
        "address": "123 Test Street, Dhaka",
        "secondary_contact": "01987654321",
        "hub_id": 1,
    },
}

STORE_LIST_SUCCESS = {
    "type": "success",
    "data": [
        {
            "store_id": 123,
            "name": "Test Store",
            "contact_name": "John Doe",
            "contact_number": "01712345678",
            "address": "123 Test Street, Dhaka",
        },
        {
            "store_id": 124,
            "name": "Another Store",
            "contact_name": "Jane Smith",
            "contact_number": "01798765432",
            "address": "456 Another Street, Dhaka",
        },
    ],
}

STORE_GET_SUCCESS = {
    "type": "success",
    "data": {
        "store_id": 123,
        "name": "Test Store",
        "contact_name": "John Doe",
        "contact_number": "01712345678",
        "address": "123 Test Street, Dhaka",
        "secondary_contact": "01987654321",
        "hub_id": 1,
    },
}

# Order responses
ORDER_CREATE_SUCCESS = {
    "type": "success",
    "data": {
        "consignment_id": "D-12345",
        "order_status": "Pending",
        "item_description": "Test Item",
        "amount_to_collect": 100.0,
        "recipient_name": "Jane Doe",
        "recipient_phone": "01712345678",
        "recipient_address": "456 Test Road, Dhaka",
    },
}

ORDER_BULK_SUCCESS = {
    "type": "success",
    "data": [
        {"consignment_id": "D-12345", "order_status": "Pending"},
        {"consignment_id": "D-12346", "order_status": "Pending"},
    ],
}

ORDER_INFO_SUCCESS = {
    "type": "success",
    "data": {
        "consignment_id": "D-12345",
        "order_status": "In Transit",
        "item_description": "Test Item",
        "amount_to_collect": 100.0,
        "recipient_name": "Jane Doe",
        "recipient_phone": "01712345678",
        "recipient_address": "456 Test Road, Dhaka",
        "tracking_history": [
            {"status": "Pending", "timestamp": "2023-01-01T10:00:00Z"},
            {"status": "In Transit", "timestamp": "2023-01-01T14:00:00Z"},
        ],
    },
}

# Location responses
CITIES_SUCCESS = {
    "type": "success",
    "data": {
        "data": [
            {"city_id": 1, "city_name": "Dhaka"},
            {"city_id": 2, "city_name": "Chittagong"},
            {"city_id": 3, "city_name": "Sylhet"},
        ]
    },
}

ZONES_SUCCESS = {
    "type": "success",
    "data": [
        {"zone_id": 1, "zone_name": "Dhanmondi", "city_id": 1},
        {"zone_id": 2, "zone_name": "Gulshan", "city_id": 1},
        {"zone_id": 3, "zone_name": "Uttara", "city_id": 1},
    ],
}

AREAS_SUCCESS = {
    "type": "success",
    "data": [
        {"area_id": 1, "area_name": "Dhanmondi 27", "zone_id": 1},
        {"area_id": 2, "area_name": "Dhanmondi 32", "zone_id": 1},
        {"area_id": 3, "area_name": "Gulshan 1", "zone_id": 2},
    ],
}

# Price responses
PRICE_SUCCESS = {
    "type": "success",
    "data": {
        "price": 60.0,
        "discount": 5.0,
        "promo_discount": 0.0,
        "cod_enabled": True,
        "cod_percentage": 1.0,
        "additional_charges": 0.0,
        "final_price": 55.0,
        "plan_id": 1,
    },
}

# Error responses
VALIDATION_ERROR = {
    "type": "error",
    "message": "Validation failed",
    "errors": {"recipient_phone": ["Invalid phone number format"]},
}

NOT_FOUND_ERROR = {"type": "error", "message": "Resource not found", "code": 404}

API_ERROR = {"type": "error", "message": "Internal server error", "code": 500}

NETWORK_ERROR = {"error": "Connection timeout"}
