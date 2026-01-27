# Pathao Python SDK - Development Guide

**For Agentic AI Code Development**

---

## Project Structure and Setup

### Directory Tree

```
pathao-python/
├── README.md                          # Project overview
├── LICENSE                            # MIT License
├── setup.py                           # Package setup
├── pyproject.toml                     # Project metadata
├── requirements.txt                   # Production dependencies
├── requirements-dev.txt               # Development dependencies
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment variables template
│
├── pathao/                            # Main package
│   ├── __init__.py                   # Package exports
│   ├── client.py                     # Main PathaoClient class
│   ├── exceptions.py                 # Custom exceptions
│   ├── models.py                     # Dataclass models
│   ├── http_client.py                # HTTP wrapper with retry logic
│   ├── validators.py                 # Input validators
│   ├── logger.py                     # Logging configuration
│   └── modules/                      # Functional modules
│       ├── __init__.py
│       ├── auth.py                   # AuthModule
│       ├── store.py                  # StoreModule
│       ├── order.py                  # OrderModule
│       ├── location.py               # LocationModule
│       └── price.py                  # PriceModule
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   ├── test_auth.py
│   ├── test_store.py
│   ├── test_order.py
│   ├── test_location.py
│   ├── test_price.py
│   ├── test_validators.py
│   ├── test_http_client.py
│   └── fixtures/
│       ├── __init__.py
│       └── mock_responses.py          # Mock API responses
│
├── examples/                         # Usage examples
│   ├── basic_usage.py
│   ├── create_order.py
│   ├── bulk_orders.py
│   ├── location_services.py
│   └── error_handling.py
│
├── docs/                             # Documentation
│   ├── index.md
│   ├── installation.md
│   ├── authentication.md
│   ├── store_management.md
│   ├── order_management.md
│   ├── location_services.md
│   ├── price_calculation.md
│   └── error_handling.md
│
└── .github/
    └── workflows/
        ├── tests.yml                 # CI/CD for tests
        └── publish.yml               # CI/CD for PyPI publishing
```

---

## Implementation Guide

### Phase 1: Setup and Configuration Files

#### 1.1 setup.py

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pathao",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python SDK for Pathao Courier Merchant API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pathao-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "pytest-mock>=3.10",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.990",
            "sphinx>=5.0",
        ]
    },
)
```

#### 1.2 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pathao"
version = "0.1.0"
description = "Python SDK for Pathao Courier Merchant API"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["pathao", "courier", "shipping", "logistics", "api"]

[project.urls]
Homepage = "https://github.com/yourusername/pathao-python"
Documentation = "https://pathao-python.readthedocs.io"
Repository = "https://github.com/yourusername/pathao-python.git"
"Bug Tracker" = "https://github.com/yourusername/pathao-python/issues"
```

#### 1.3 .env.example

```bash
# Pathao API Credentials
PATHAO_CLIENT_ID=your_client_id_here
PATHAO_CLIENT_SECRET=your_client_secret_here
PATHAO_USERNAME=your_email@example.com
PATHAO_PASSWORD=your_password_here

# Environment: sandbox or production
PATHAO_ENVIRONMENT=sandbox

# Optional: Request timeout (seconds)
PATHAO_TIMEOUT=30

# Optional: Max retries for failed requests
PATHAO_MAX_RETRIES=3
```

#### 1.4 requirements.txt

```
requests>=2.28.0
python-dotenv>=0.21.0
```

#### 1.5 requirements-dev.txt

```
pytest>=7.0
pytest-cov>=4.0
pytest-mock>=3.10
black>=22.0
flake8>=4.0
mypy>=0.990
sphinx>=5.0
wheel>=0.37.0
twine>=3.8.0
```

---

### Phase 2: Core Exceptions and Models

#### 2.1 exceptions.py

Define all custom exception classes with proper hierarchy and useful attributes.

**Key Classes:**
- `PathaoException` - Base exception
- `AuthenticationError` - Auth failures
- `ValidationError` - Input validation failures
- `NotFoundError` - Resource not found
- `APIError` - API errors with status codes
- `NetworkError` - Network failures with retry info
- `ConfigurationError` - Configuration issues

**Methods to implement:**
- Custom `__str__()` for readable error messages
- `__repr__()` for debugging

#### 2.2 models.py

Define all dataclass models using Python's dataclasses module.

**Model Groups:**

1. **Authentication**
   - `AuthToken` - with `is_expired()` and `will_expire_soon()` methods

2. **Store Models**
   - `Store` - Single store
   - `StoreList` - List with pagination

3. **Order Models**
   - `Order` - Order response
   - `OrderInfo` - Order info response
   - `BulkOrderResponse` - Bulk order response

4. **Location Models**
   - `City`, `CityList`
   - `Zone`, `ZoneList`
   - `Area`, `AreaList`

5. **Price Models**
   - `PriceDetails` - Price calculation response

**Implementation Notes:**
- Use `@dataclass` decorator
- Use `field()` for defaults
- Add type hints for all fields
- Use `datetime` for timestamp fields
- Implement `__post_init__()` for field validation if needed

---

### Phase 3: Utilities and Validators

#### 3.1 validators.py

**Validation Functions to Implement:**

```python
def validate_name(value: str, min_length: int = 3, max_length: int = 50) -> str
def validate_phone(value: str, length: int = 11) -> str
def validate_address(value: str, min_length: int = 10, max_length: int = 220) -> str
def validate_email(value: str) -> str
def validate_weight(value: float, min_weight: float = 0.5, max_weight: float = 10.0) -> float
def validate_quantity(value: int) -> int
def validate_delivery_type(value: int) -> int
def validate_item_type(value: int) -> int
def validate_integer_range(value: int, min_val: int, max_val: int, field_name: str) -> int
```

**Validation Pattern:**
- Check for None/empty
- Check constraints (length, range, format)
- Raise `ValidationError` with field name and constraint message
- Return cleaned/normalized value

#### 3.2 logger.py

**Setup logging configuration:**

```python
def get_logger(name: str) -> logging.Logger
def setup_logging(level: str = "INFO") -> None
```

**Features:**
- Support different log levels
- Format: timestamp, logger name, level, message
- Optional file output
- Exclude sensitive data (tokens, passwords)

---

### Phase 4: HTTP Client Layer

#### 4.1 http_client.py

**HTTPClient Class:**

```python
class HTTPClient:
    """Wrapper around requests library with retry logic."""
    
    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3, retry_backoff: float = 0.3)
    def get(self, endpoint: str, headers: dict = None, params: dict = None) -> dict
    def post(self, endpoint: str, headers: dict = None, data: dict = None) -> dict
    def _make_request(self, method: str, endpoint: str, ...) -> dict
    def _should_retry(self, exception: Exception, attempt: int) -> bool
    def _exponential_backoff(self, attempt: int) -> None
```

**Features:**
- Base URL management
- URL construction
- JSON serialization/deserialization
- Error handling and response parsing
- Exponential backoff retry logic
- Request timeout handling
- Logging of requests/responses (without sensitive data)

---

### Phase 5: Authentication Module

#### 5.1 auth.py - AuthModule Class

**Core Functionality:**

```python
class AuthModule:
    def __init__(self, http_client: HTTPClient, credentials: dict)
    def get_access_token(self) -> str
    def refresh_token(self) -> AuthToken
    def _issue_token(self, grant_type: str, **kwargs) -> AuthToken
    def is_token_valid(self) -> bool
    def is_token_expiring_soon(self, seconds: int = 300) -> bool
    def _store_token(self, token: AuthToken) -> None
    def _load_token(self) -> AuthToken
```

**Key Features:**
- OAuth 2.0 password grant flow
- Token refresh flow
- In-memory token storage
- Automatic token refresh before expiration
- Token expiration checking

---

### Phase 6: Store Management Module

#### 6.1 store.py - StoreModule Class

**Core Methods:**

```python
class StoreModule:
    def create(self, name: str, contact_name: str, ...) -> Store
    def list(self, page: int = 1, per_page: int = 100) -> StoreList
    def get(self, store_id: int) -> Store
```

**Implementation Pattern:**
1. Validate input parameters
2. Make HTTP request via HTTPClient
3. Parse response into model
4. Return model object

---

### Phase 7: Order Management Module

#### 7.1 order.py - OrderModule Class

**Core Methods:**

```python
class OrderModule:
    def create(self, store_id: int, recipient_name: str, ...) -> Order
    def create_bulk(self, orders: List[Dict]) -> BulkOrderResponse
    def get_info(self, consignment_id: str) -> OrderInfo
    def _normalize_delivery_type(self, delivery_type: int) -> int
    def _prepare_order_payload(self, **kwargs) -> dict
```

**Validation Strategy:**
- Validate each parameter individually
- Build payload dictionary
- Send to API
- Handle 200 or 202 responses differently

---

### Phase 8: Location Services Module

#### 8.1 location.py - LocationModule Class

**Core Methods:**

```python
class LocationModule:
    def get_cities(self) -> CityList
    def get_zones(self, city_id: int) -> ZoneList
    def get_areas(self, zone_id: int) -> AreaList
    def get_city_by_name(self, name: str) -> City
```

**Features:**
- Caching of location data (optional)
- Lazy loading of location hierarchy
- Case-insensitive name searches

---

### Phase 9: Price Module

#### 9.1 price.py - PriceModule Class

**Core Methods:**

```python
class PriceModule:
    def calculate(self, store_id: int, item_type: int, delivery_type: int, 
                  item_weight: float, recipient_city: int, recipient_zone: int) -> PriceDetails
```

---

### Phase 10: Main Client Class

#### 10.1 client.py - PathaoClient Class

**Main Entry Point:**

```python
class PathaoClient:
    def __init__(self, client_id: str = None, client_secret: str = None, 
                 username: str = None, password: str = None,
                 environment: str = "sandbox", timeout: int = 30,
                 max_retries: int = 3, retry_backoff: float = 0.3)
    
    @property
    def stores(self) -> StoreModule
    @property
    def orders(self) -> OrderModule
    @property
    def locations(self) -> LocationModule
    @property
    def prices(self) -> PriceModule
    
    def get_access_token(self) -> str
    def refresh_token(self) -> None
    def is_token_valid(self) -> bool
    
    def _load_credentials_from_env(self) -> dict
    def _validate_credentials(self) -> None
    def _initialize_modules(self) -> None
```

**Features:**
- Load credentials from parameters or .env
- Initialize all modules
- Delegate to appropriate modules via properties
- Manage shared HTTPClient and AuthModule

---

### Phase 11: Package Initialization

#### 11.1 pathao/__init__.py

**Public API:**

```python
from pathao.client import PathaoClient
from pathao.exceptions import (
    PathaoException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
)
from pathao.models import (
    # All model classes
)

__version__ = "0.1.0"
__all__ = [
    "PathaoClient",
    # Exception classes
    # Model classes
]
```

---

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── fixtures/
│   └── mock_responses.py    # Mock API responses
├── test_auth.py             # Auth module tests
├── test_store.py            # Store module tests
├── test_order.py            # Order module tests
├── test_location.py         # Location module tests
├── test_price.py            # Price module tests
├── test_validators.py       # Validator tests
└── test_http_client.py      # HTTP client tests
```

### Test Patterns

#### Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch
from pathao.modules.store import StoreModule
from pathao.exceptions import ValidationError

def test_store_create_success(mock_http_client):
    """Test successful store creation."""
    # Arrange
    module = StoreModule(mock_http_client)
    expected_response = {
        "message": "Store created successfully",
        "data": {"store_name": "Test Store"}
    }
    mock_http_client.post.return_value = expected_response
    
    # Act
    result = module.create(
        name="Test Store",
        contact_name="John Doe",
        contact_number="01712345678",
        address="Test Address, City",
        city_id=1,
        zone_id=298,
        area_id=37
    )
    
    # Assert
    assert result.store_name == "Test Store"
    mock_http_client.post.assert_called_once()

def test_store_create_invalid_name():
    """Test store creation with invalid name."""
    module = StoreModule(Mock())
    
    with pytest.raises(ValidationError) as exc_info:
        module.create(
            name="AB",  # Too short
            # ... other params
        )
    
    assert "name" in str(exc_info.value).lower()
```

### Mocking Strategy

Use fixtures for:
- Mock HTTP client
- Mock responses
- Test data
- Authentication tokens

---

## CI/CD Configuration

### GitHub Actions - tests.yml

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    - name: Lint
      run: |
        flake8 pathao
        black --check pathao
    - name: Type check
      run: mypy pathao
    - name: Test
      run: pytest --cov=pathao tests/
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### GitHub Actions - publish.yml

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build
      run: python -m build
    - name: Publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

---

## Code Style and Quality Standards

### PEP 8 Compliance

- Use 4-space indentation
- Max line length: 88 (Black formatter)
- Use type hints for all functions
- Document public classes and methods with docstrings

### Docstring Format (Google Style)

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

## Development Workflow

### For AI Code Generation

When requesting AI to generate code:

1. **Specify the file:** `Generate pathao/modules/auth.py`
2. **Include context:** Which models, exceptions, and utilities to import
3. **Provide examples:** Show expected behavior
4. **Define error handling:** What exceptions to raise when
5. **Include docstrings:** Full documentation

### Command to generate with AI:

```
Generate the [module_name] module with:
- Classes: [list]
- Methods: [list with signatures]
- Error handling: [list of exceptions]
- Tests: [test patterns to follow]
```

---

## Performance Considerations

- Token caching to avoid repeated auth
- Location data caching to reduce API calls
- HTTP connection pooling via requests
- Efficient JSON parsing
- Minimal dependencies

---

## Security Considerations

- Never log tokens or passwords
- Validate SSL certificates
- Use HTTPS only
- Sanitize error messages
- Secure credential storage guidance in docs
- Input validation before API calls

---

## Deployment Checklist

- [ ] All tests passing
- [ ] 80%+ code coverage
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Documentation complete
- [ ] Examples tested
- [ ] Changelog updated
- [ ] Version bumped
- [ ] PyPI credentials configured
- [ ] GitHub Actions configured
- [ ] License headers added
- [ ] Contributing guidelines written

---

**End of Development Guide**
