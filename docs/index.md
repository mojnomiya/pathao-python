---
layout: home
title: Home
---

# Pathao Python SDK

[![Tests](https://github.com/mojnomiya/pathao-python/workflows/Tests/badge.svg)](https://github.com/mojnomiya/pathao-python/actions)
[![PyPI version](https://badge.fury.io/py/pathao.svg)](https://badge.fury.io/py/pathao)
[![Python versions](https://img.shields.io/pypi/pyversions/pathao.svg)](https://pypi.org/project/pathao/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python SDK for the Pathao Courier Merchant API. This package provides a clean, Pythonic interface to integrate Pathao's courier services into your Python applications.

## ✨ Features

- 🔐 **OAuth 2.0 Authentication** - Automatic token refresh
- 🎯 **Type Hints** - Full type safety throughout
-  **Input Validation** - Comprehensive validation with detailed error messages
- 🌍 **Multi-Environment** - Support for Sandbox and Production
- 📦 **Batch Operations** - Efficient bulk operations
- 📚 **Extensive Documentation** - Complete guides and examples
- 🧪 **97% Test Coverage** - Thoroughly tested codebase

## 🚀 Quick Start

### Installation

```bash
pip install pathao
```

### Basic Usage

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

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [Installation](installation.html) | Installation and setup instructions |
| [Authentication](authentication.html) | OAuth 2.0 authentication setup |
| [Store Management](store_management.html) | Managing your stores |
| [Order Management](order_management.html) | Creating and managing orders |
| [Location Services](location_services.html) | Working with cities, zones, and areas |
| [Price Calculation](price_calculation.html) | Calculating delivery prices |
| [Error Handling](error_handling.html) | Handling errors and exceptions |
| [API Reference](api_reference.html) | Complete API documentation |

## 🛠️ Requirements

- Python 3.8 or higher
- `requests>=2.28.0`
- `python-dotenv>=0.21.0`

## 📊 Project Stats

- **196 Tests** with **97% Coverage**
- **15 Development Phases** completed
- **8 Comprehensive Guides** + **3 Examples**
- **Full Type Safety** with mypy
- **Production Ready** with CI/CD pipeline

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/mojnomiya/pathao-python/blob/main/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/mojnomiya/pathao-python/blob/main/LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/mojnomiya/pathao-python)
- [PyPI Package](https://pypi.org/project/pathao/)
- [Issue Tracker](https://github.com/mojnomiya/pathao-python/issues)
