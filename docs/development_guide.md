# Pathao Python SDK - Development Guide

**For Contributors and Maintainers**
**Status:** Complete Implementation ✅

---

## Project Overview

The Pathao Python SDK is a production-ready Python package that provides a comprehensive interface to the Pathao Courier Merchant API. This guide covers the architecture, implementation details, and development workflow for contributors.

### Implementation Status ✅

- ✅ **Complete Implementation:** All 15 phases completed
- ✅ **Test Coverage:** 97% with 196 unit tests
- ✅ **Code Quality:** Zero linting/type errors
- ✅ **Documentation:** 8 comprehensive guides + 3 examples
- ✅ **CI/CD:** Automated testing and quality checks
- ✅ **Release Ready:** Version 0.1.0 prepared for PyPI

---

## Project Structure

### Directory Tree ✅

```
pathao-python/
├── README.md                          ✅ Project overview
├── LICENSE                            ✅ MIT License
├── setup.py                           ✅ Package setup
├── pyproject.toml                     ✅ Project metadata
├── requirements.txt                   ✅ Production dependencies
├── requirements-dev.txt               ✅ Development dependencies
├── .gitignore                         ✅ Git ignore rules
├── .env.example                       ✅ Environment variables template
├── CHANGELOG.md                       ✅ Version history
├── CONTRIBUTING.md                    ✅ Development guidelines
├── CODE_OF_CONDUCT.md                 ✅ Community standards
│
├── pathao/                            ✅ Main package
│   ├── __init__.py                   ✅ Package exports
│   ├── client.py                     ✅ Main PathaoClient class
│   ├── exceptions.py                 ✅ Custom exceptions (7 types)
│   ├── models.py                     ✅ Dataclass models (15 models)
│   ├── http_client.py                ✅ HTTP wrapper with retry logic
│   ├── validators.py                 ✅ Input validators (9 functions)
│   ├── logger.py                     ✅ Secure logging configuration
│   └── modules/                      ✅ Functional modules
│       ├── __init__.py
│       ├── auth.py                   ✅ OAuth 2.0 AuthModule
│       ├── store.py                  ✅ StoreModule
│       ├── order.py                  ✅ OrderModule
│       ├── location.py               ✅ LocationModule
│       └── price.py                  ✅ PriceModule
│
├── tests/                            ✅ Test suite (196 tests, 97% coverage)
│   ├── __init__.py
│   ├── conftest.py                   ✅ Pytest configuration
│   ├── test_*.py                     ✅ Unit tests for all modules
│   ├── test_integration*.py          ✅ Integration tests
│   └── fixtures/
│       ├── __init__.py
│       └── mock_responses.py          ✅ Mock API responses
│
├── examples/                         ✅ Usage examples
│   ├── basic_usage.py                ✅ Getting started
│   ├── create_order.py               ✅ Order workflow
│   └── error_handling.py             ✅ Error patterns
│
├── docs/                             ✅ Documentation
│   ├── index.md                      ✅ Documentation home
│   ├── installation.md               ✅ Setup guide
│   ├── authentication.md             ✅ Auth guide
│   ├── store_management.md           ✅ Store API
│   ├── order_management.md           ✅ Order API
│   ├── location_services.md          ✅ Location API
│   ├── price_calculation.md          ✅ Price API
│   ├── error_handling.md             ✅ Error guide
│   ├── srs.md                        ✅ Requirements specification
│   ├── api_reference.md              ✅ Complete API reference
│   └── development_guide.md          ✅ This guide
│
└── .github/                          ✅ CI/CD and templates
    ├── workflows/
    │   ├── tests.yml                 ✅ Multi-Python testing
    │   ├── quality.yml               ✅ Code quality checks
    │   └── publish.yml               ✅ PyPI publishing
    ├── ISSUE_TEMPLATE/               ✅ Issue templates
    ├── dependabot.yml                ✅ Dependency updates
    └── pull_request_template.md      ✅ PR template
```

---

## Architecture Overview

### System Architecture ✅

```
┌─────────────────────────────────────────┐
│     User Application                    │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Pathao Python SDK (v0.1.0)           │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │  PathaoClient (client.py)       │   │
│  │  • Credential Management        │   │
│  │  • Environment Support          │   │
│  │  • Module Initialization        │   │
│  └────────────┬────────────────────┘   │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Service Modules                 │ │
│  │ ├─ AuthModule (auth.py)          │ │
│  │ │  • OAuth 2.0 flows             │ │
│  │ │  • Token lifecycle mgmt        │ │
│  │ ├─ StoreModule (store.py)        │ │
│  │ │  • CRUD operations             │ │
│  │ ├─ OrderModule (order.py)        │ │
│  │ │  • Single/bulk creation        │ │
│  │ │  • Order tracking              │ │
│  │ ├─ LocationModule (location.py)  │ │
│  │ │  • Location hierarchy          │ │
│  │ └─ PriceModule (price.py)        │ │
│  │    • Price calculation           │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  HTTPClient (http_client.py)     │ │
│  │  • Exponential backoff retry     │ │
│  │  • JSON serialization            │ │
│  │  • Error handling & conversion   │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Core Utilities                  │ │
│  │ ├─ Validators (validators.py)     │ │
│  │ │  • Input validation (9 funcs)  │ │
│  │ ├─ Exceptions (exceptions.py)    │ │
│  │ │  • Custom hierarchy (7 types)  │ │
│  │ ├─ Models (models.py)            │ │
│  │ │  • Dataclasses (15 models)     │ │
│  │ └─ Logger (logger.py)            │ │
│  │    • Secure logging w/ masking   │ │
│  └──────────────────────────────────┘ │
└─────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Pathao Courier API                    │
│  (Sandbox / Production)                 │
└─────────────────────────────────────────┘
```

---

## Implementation Details

### Core Components

#### 1. Exception Hierarchy ✅

**File:** `pathao/exceptions.py`

```python
PathaoException (base)
├── AuthenticationError    # OAuth failures, token issues
├── ValidationError        # Input validation failures
├── NotFoundError         # Resource not found (404)
├── APIError             # General API errors with status codes
├── NetworkError         # Network/connection issues
└── ConfigurationError   # Missing/invalid configuration
```

**Features:**
- Descriptive error messages with context
- Status code preservation for API errors
- Field-specific validation error details
- Retry information for network errors

#### 2. Data Models ✅

**File:** `pathao/models.py`

**15 Dataclass Models:**
- `AuthToken` - OAuth token with expiration methods
- `Store`, `StoreList` - Store management
- `Order`, `OrderInfo`, `BulkOrderResponse` - Order operations
- `City`, `CityList`, `Zone`, `ZoneList`, `Area`, `AreaList` - Location hierarchy
- `PriceDetails` - Price calculation results

**Features:**
- Type hints throughout
- Custom methods for business logic
- JSON serialization support
- Validation in `__post_init__` where needed

#### 3. Input Validation ✅

**File:** `pathao/validators.py`

**9 Validation Functions:**
- `validate_name()` - Name length validation (3-50 chars)
- `validate_phone()` - Phone format validation (11 digits)
- `validate_address()` - Address length validation (10-220 chars)
- `validate_email()` - Email format validation
- `validate_weight()` - Weight range validation (0.5-10 kg)
- `validate_quantity()` - Positive integer validation
- `validate_delivery_type()` - Enum validation (12, 48)
- `validate_item_type()` - Enum validation (1, 2)
- `validate_integer_range()` - Generic range validation

#### 4. HTTP Client ✅

**File:** `pathao/http_client.py`

**Features:**
- Exponential backoff retry logic (configurable)
- Smart retry decisions (5xx yes, 4xx no)
- Automatic JSON serialization/deserialization
- Comprehensive error handling and conversion
- Request/response logging (non-sensitive data)
- Session-based connection pooling

#### 5. Authentication Module ✅

**File:** `pathao/modules/auth.py`

**OAuth 2.0 Implementation:**
- Password grant flow for initial authentication
- Refresh token grant flow for token renewal
- Automatic token refresh (5 minutes before expiry)
- Intelligent fallback to password grant if refresh fails
- Thread-safe in-memory token storage

#### 6. Service Modules ✅

**Store Module** (`pathao/modules/store.py`):
- Create stores with comprehensive validation
- List stores with pagination
- Get individual store details

**Order Module** (`pathao/modules/order.py`):
- Single order creation with 13 parameters
- Bulk order creation with batch processing
- Order tracking by consignment ID

**Location Module** (`pathao/modules/location.py`):
- Cities, zones, areas hierarchy
- Case-insensitive city search
- Service availability flags

**Price Module** (`pathao/modules/price.py`):
- Delivery price calculation
- Complete price breakdown
- COD availability and charges

---

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/pathao-python.git
cd pathao-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pathao --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run integration tests (requires sandbox credentials)
pytest tests/test_integration_sandbox.py
```

### Code Quality Checks

```bash
# Format code
black pathao tests

# Check formatting
black --check pathao tests

# Lint code
flake8 pathao tests

# Type checking
mypy pathao

# Run all quality checks
pre-commit run --all-files
```

### Testing Strategy

#### Unit Tests (196 tests, 97% coverage) ✅

**Test Structure:**
```
tests/
├── conftest.py              # Shared fixtures
├── fixtures/
│   └── mock_responses.py    # Mock API responses
├── test_auth.py             # Auth module (25 tests)
├── test_store.py            # Store module (12 tests)
├── test_order.py            # Order module (11 tests)
├── test_location.py         # Location module (15 tests)
├── test_price.py            # Price module (7 tests)
├── test_validators.py       # Validators (27 tests)
├── test_exceptions.py       # Exceptions (7 tests)
├── test_models.py           # Models (15 tests)
├── test_http_client.py      # HTTP client (24 tests)
├── test_client.py           # Main client (13 tests)
├── test_logger.py           # Logger (5 tests)
├── test_integration.py      # Integration tests (20 tests)
└── test_integration_sandbox.py # Real API tests (15 tests)
```

**Testing Patterns:**
- Comprehensive mocking with `unittest.mock`
- Fixture-based test data
- Parametrized tests for multiple scenarios
- Error condition testing
- Integration tests with real sandbox API

#### Integration Tests ✅

**Real Sandbox Testing:**
- Authentication flow validation
- All API endpoints tested
- Error handling verification
- Concurrent operation testing
- Environment configuration testing

### Code Style Standards ✅

#### PEP 8 Compliance
- 4-space indentation
- 88-character line length (Black formatter)
- Type hints for all functions
- Google-style docstrings

#### Example Docstring Format:

```python
def create_order(self, store_id: int, recipient_name: str) -> Order:
    """Create a new order.

    Args:
        store_id: The store ID from which the order is created.
        recipient_name: Name of the order recipient.

    Returns:
        Order object containing order details.

    Raises:
        ValidationError: If parameters are invalid.
        APIError: If API request fails.

    Examples:
        >>> order = client.orders.create(1, "John Doe", ...)
        >>> print(order.consignment_id)
    """
```

---

## CI/CD Pipeline ✅

### GitHub Actions Workflows

#### 1. Tests Workflow (`.github/workflows/tests.yml`) ✅

```yaml
# Runs on: push, pull_request
# Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
# Steps:
#   - Code formatting check (Black)
#   - Linting (flake8)
#   - Type checking (mypy)
#   - Unit tests with coverage
#   - Coverage upload to Codecov
```

#### 2. Quality Workflow (`.github/workflows/quality.yml`) ✅

```yaml
# Runs on: push, pull_request
# Steps:
#   - Pre-commit hooks
#   - Security scanning
#   - Dependency checking
```

#### 3. Publish Workflow (`.github/workflows/publish.yml`) ✅

```yaml
# Runs on: release creation
# Steps:
#   - Build package
#   - Publish to PyPI
#   - Create GitHub release
```

### Pre-commit Hooks ✅

**Configuration:** `.pre-commit-config.yaml`

- Black code formatting
- Flake8 linting
- Mypy type checking
- Trailing whitespace removal
- YAML validation
- Large file prevention

---

## Release Management

### Version Strategy ✅

**Semantic Versioning (MAJOR.MINOR.PATCH):**
- Current version: `0.1.0` (alpha release)
- Stable release target: `1.0.0`

**Version Locations:**
- `setup.py`
- `pyproject.toml`
- `pathao/__init__.py`

### Release Process ✅

1. **Update version** in all locations
2. **Update CHANGELOG.md** with new features/fixes
3. **Run full test suite** and quality checks
4. **Create git tag** with version (e.g., `v0.1.0`)
5. **Push tag** to trigger automated PyPI publishing
6. **Create GitHub release** with release notes

### PyPI Publishing ✅

**Automated via GitHub Actions:**
- Triggered on release creation
- Builds source and wheel distributions
- Publishes to PyPI using trusted publishing
- Creates GitHub release with artifacts

---

## Contributing Guidelines

### Development Process

1. **Fork repository** and create feature branch
2. **Make changes** following code style guidelines
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Run quality checks** locally
6. **Submit pull request** with clear description

### Pull Request Requirements ✅

- [ ] All tests passing
- [ ] Code coverage maintained (>95%)
- [ ] No linting or type errors
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventional format

### Issue Templates ✅

**Bug Report Template:**
- Environment information
- Steps to reproduce
- Expected vs actual behavior
- Code samples

**Feature Request Template:**
- Use case description
- Proposed solution
- Alternative solutions considered
- Additional context

---

## Security Considerations ✅

### Implemented Security Measures

1. **Credential Protection:**
   - Sensitive data masking in logs
   - No credentials in error messages
   - Secure in-memory token storage

2. **Network Security:**
   - HTTPS-only communication
   - SSL certificate validation
   - Request timeout protection

3. **Input Validation:**
   - Comprehensive parameter validation
   - SQL injection prevention
   - XSS protection in error messages

4. **Dependency Security:**
   - Minimal dependency footprint
   - Regular dependency updates via Dependabot
   - Security scanning in CI/CD

---

## Performance Considerations ✅

### Optimization Strategies

1. **HTTP Efficiency:**
   - Connection pooling via requests sessions
   - Configurable timeouts and retries
   - Efficient JSON parsing

2. **Memory Management:**
   - Lightweight dataclass models
   - Efficient token storage
   - Minimal object creation

3. **API Efficiency:**
   - Bulk operations support
   - Location data caching capability
   - Smart retry logic to avoid unnecessary calls

---

## Troubleshooting

### Common Issues

#### Authentication Problems
```python
# Check token validity
if not client.is_token_valid():
    client.refresh_token()

# Verify credentials
try:
    token = client.get_access_token()
    print("Authentication successful")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
```

#### Network Issues
```python
# Configure retry settings
client = PathaoClient(
    max_retries=5,
    retry_backoff=0.5,
    timeout=60
)
```

#### Validation Errors
```python
from pathao.exceptions import ValidationError

try:
    order = client.orders.create(...)
except ValidationError as e:
    print(f"Field '{e.field}' failed validation: {e.message}")
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
client = PathaoClient(...)
# All HTTP requests/responses will be logged
```

---

## Future Enhancements

### Planned Features (v1.1+)

1. **Caching Layer:**
   - Location data caching
   - Token persistence options
   - Response caching for read operations

2. **Advanced Features:**
   - Webhook support for order updates
   - Batch operation status tracking
   - Advanced retry strategies

3. **Developer Experience:**
   - CLI tool for common operations
   - Django/Flask integration helpers
   - Async support (asyncio)

4. **Monitoring:**
   - Metrics collection
   - Performance monitoring
   - Health check endpoints

---

## Conclusion

The Pathao Python SDK represents a complete, production-ready implementation that exceeds the original requirements. With 97% test coverage, comprehensive documentation, and robust error handling, it provides a solid foundation for Python developers integrating with Pathao's courier services.

The modular architecture, extensive testing, and automated CI/CD pipeline ensure maintainability and reliability for long-term use and community contributions.

---

**Guide Status:** ✅ Complete - Reflects current implementation
**Last Updated:** January 2026
**SDK Version:** 0.1.0
