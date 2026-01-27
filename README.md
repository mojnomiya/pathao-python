# Pathao Python SDK

[![Tests](https://github.com/yourusername/pathao-python/workflows/Tests/badge.svg)](https://github.com/yourusername/pathao-python/actions)
[![PyPI version](https://badge.fury.io/py/pathao.svg)](https://badge.fury.io/py/pathao)
[![Python versions](https://img.shields.io/pypi/pyversions/pathao.svg)](https://pypi.org/project/pathao/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python SDK for the Pathao Courier Merchant API. This package provides a clean, Pythonic interface to integrate Pathao's courier services into your Python applications.

## Features

- ✅ OAuth 2.0 authentication with automatic token refresh
- ✅ Type hints throughout the codebase
- ✅ Comprehensive input validation
- ✅ Detailed error messages
- ✅ Support for both Sandbox and Production environments
- ✅ Batch operations support
- ✅ Extensive documentation and examples

## Installation

```bash
pip install pathao
```

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
    recipient_name="John Doe",
    recipient_phone="01712345678",
    recipient_address="House 123, Road 4, Dhaka",
    delivery_type=48,  # Normal delivery
    item_type=2,  # Parcel
    item_quantity=1,
    item_weight=0.5,
    amount_to_collect=0
)

print(f"Order created: {order.consignment_id}")
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Authentication](docs/authentication.md)
- [Store Management](docs/store_management.md)
- [Order Management](docs/order_management.md)
- [Location Services](docs/location_services.md)
- [Price Calculation](docs/price_calculation.md)
- [Error Handling](docs/error_handling.md)

## Requirements

- Python 3.8 or higher
- `requests>=2.28.0`
- `python-dotenv>=0.21.0`

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/pathao-python.git
cd pathao-python

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black pathao tests

# Type checking
mypy pathao
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [GitHub Issues](https://github.com/yourusername/pathao-python/issues)
- [Documentation](https://pathao-python.readthedocs.io)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and releases.
