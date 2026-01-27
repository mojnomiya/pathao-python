# Pathao Python SDK Documentation

Welcome to the comprehensive documentation for the Pathao Python SDK. This SDK provides a clean, Pythonic interface to integrate Pathao's courier services into your Python applications.

## Quick Start

```python
from pathao import PathaoClient

# Initialize the client
client = PathaoClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_email",
    password="your_password",
    environment="sandbox"  # Use "production" for live
)

# Create an order
order = client.orders.create(
    store_id=1,
    merchant_order_id="ORDER-001",
    recipient_name="John Doe",
    recipient_phone="01712345678",
    recipient_address="House 123, Road 4, Dhaka",
    recipient_city=1,
    recipient_zone=1,
    delivery_type=48,  # Normal delivery
    item_type=2,       # Parcel
    item_quantity=1,
    item_weight=0.5,
    amount_to_collect=0
)

print(f"Order created: {order.consignment_id}")
```

## Features

- ✅ **OAuth 2.0 Authentication** - Automatic token management and refresh
- ✅ **Type Hints** - Full type annotations throughout the codebase
- ✅ **Input Validation** - Comprehensive validation with detailed error messages
- ✅ **Error Handling** - Specific exception types for different error scenarios
- ✅ **Environment Support** - Both Sandbox and Production environments
- ✅ **Retry Logic** - Automatic retry with exponential backoff for network issues
- ✅ **Comprehensive Testing** - 196+ unit tests with integration test support

## API Modules

### 🏪 Store Management
Manage pickup locations for your orders.
- Create stores with location validation
- List stores with pagination
- Get store details

### 📦 Order Management  
Create and track delivery orders.
- Single order creation
- Bulk order processing
- Order tracking and status updates

### 📍 Location Services
Access city, zone, and area information.
- Get all cities
- Get zones by city
- Get areas by zone
- Search cities by name

### 💰 Price Calculation
Calculate delivery costs before order creation.
- Normal vs Express delivery pricing
- Weight-based pricing
- COD availability and fees

## Documentation Sections

### Getting Started
- [Installation Guide](installation.md) - Setup and installation instructions
- [Authentication](authentication.md) - Credential management and OAuth setup

### API Guides
- [Store Management](store_management.md) - Store creation and management
- [Order Management](order_management.md) - Order creation and tracking
- [Location Services](location_services.md) - Location hierarchy and search
- [Price Calculation](price_calculation.md) - Delivery cost calculation
- [Error Handling](error_handling.md) - Exception handling patterns

### Examples
- [Basic Usage](../examples/basic_usage.py) - Simple getting started example
- [Create Order](../examples/create_order.py) - Order creation walkthrough
- [Error Handling](../examples/error_handling.py) - Error handling patterns

## API Reference

### PathaoClient

Main client class providing access to all Pathao services.

```python
class PathaoClient:
    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        username: str = None,
        password: str = None,
        environment: str = "sandbox"
    )
    
    # Service modules
    stores: StoreModule
    orders: OrderModule
    locations: LocationModule
    prices: PriceModule
    
    # Token management
    def get_access_token() -> str
    def refresh_token() -> None
    def is_token_valid() -> bool
```

### Exception Hierarchy

```python
PathaoException                 # Base exception
├── AuthenticationError        # Authentication failures
├── ValidationError           # Input validation errors
├── NotFoundError            # Resource not found
├── APIError                 # API server errors
├── NetworkError             # Network/connection issues
└── ConfigurationError       # Configuration problems
```

### Data Models

All API responses are returned as typed dataclass objects:

- `Store` - Store information
- `Order` - Order creation response
- `OrderInfo` - Order tracking information
- `City`, `Zone`, `Area` - Location data
- `PriceDetails` - Price calculation results

## Environment Configuration

### Sandbox Environment
- For testing and development
- Base URL: `https://courier-api-sandbox.pathao.com`
- Use `environment="sandbox"`

### Production Environment
- For live operations
- Base URL: `https://api.pathao.com`
- Use `environment="production"`

## Best Practices

1. **Use Environment Variables** - Don't hardcode credentials
2. **Start with Sandbox** - Test thoroughly before production
3. **Handle Errors Gracefully** - Use specific exception types
4. **Validate Inputs** - Check data before API calls
5. **Implement Retry Logic** - Handle network issues automatically
6. **Cache Location Data** - Location data changes infrequently

## Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/pathao-python/issues)
- **Documentation**: This comprehensive guide
- **Examples**: Working code examples in the `examples/` directory

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](../CONTRIBUTING.md) for details on:
- Code style and formatting
- Testing requirements
- Pull request process
- Development setup

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.