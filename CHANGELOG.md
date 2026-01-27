# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-27

### Added
- Initial release of Pathao Python SDK
- OAuth 2.0 authentication with automatic token management
- Store management (create, list, get stores)
- Order management (create single/bulk orders, track orders)
- Location services (cities, zones, areas with search)
- Price calculation (delivery cost estimation)
- Comprehensive input validation
- Type hints throughout the codebase
- Retry logic with exponential backoff
- Secure logging with sensitive data masking
- Support for both Sandbox and Production environments
- Environment variable and .env file support
- Comprehensive error handling with specific exception types
- 97% test coverage with 196+ unit tests
- Integration tests for real API workflows
- Complete documentation with examples
- CI/CD pipeline with automated testing and publishing

### Features
- **PathaoClient**: Main client class with unified API access
- **Authentication**: Automatic OAuth 2.0 token management and refresh
- **Store Management**: Create, list, and retrieve store information
- **Order Management**: Single and bulk order creation with tracking
- **Location Services**: City, zone, and area lookup with search
- **Price Calculation**: Delivery cost calculation with detailed breakdown
- **Error Handling**: Comprehensive exception hierarchy
- **Validation**: Input validation for all API parameters
- **Logging**: Secure logging with sensitive data protection
- **Testing**: Extensive test suite with mocking and integration tests
- **Documentation**: Complete API documentation with examples

### Technical Details
- Python 3.8+ support
- Type hints and mypy compatibility
- Black code formatting
- Flake8 linting compliance
- Comprehensive docstrings
- Modular architecture with clean separation of concerns
- HTTP client with retry logic and error handling
- Environment-based configuration (sandbox/production)

[Unreleased]: https://github.com/yourusername/pathao-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/pathao-python/releases/tag/v0.1.0
