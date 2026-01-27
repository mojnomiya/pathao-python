# Software Requirements Specification (SRS)
## Pathao Courier Python SDK

**Document Version:** 1.0  
**Date:** January 2026  
**Author:** Development Team  
**Status:** Draft

---

## 1. Executive Summary

This document specifies the requirements for developing a comprehensive Python SDK for the Pathao Courier Merchant API. The SDK will provide developers with an easy-to-use, well-documented interface to integrate Pathao's courier services into their Python applications. The package will be published on PyPI and made available as open-source software.

---

## 2. Project Overview

### 2.1 Purpose
Create a user-friendly Python wrapper around Pathao Courier's REST API that abstracts away HTTP complexities and provides Pythonic interfaces for all Pathao operations.

### 2.2 Scope
- **In Scope:**
  - Authentication (OAuth 2.0 with token refresh)
  - Store management (create, list, retrieve)
  - Order management (single, bulk, retrieve)
  - Location services (cities, zones, areas)
  - Price calculation
  - Order tracking information
  - Support for both Sandbox and Production environments
  - Comprehensive error handling and logging
  - Type hints throughout the codebase
  - Unit and integration tests
  - Complete API documentation
  - Usage examples and tutorials

- **Out of Scope:**
  - Web UI/Dashboard
  - Real-time tracking websocket support (initial release)
  - Advanced analytics features
  - Multi-language documentation (English only for v1.0)

### 2.3 Target Users
- Python developers integrating Pathao services
- E-commerce platforms
- Logistics management systems
- Third-party shipping integrators

---

## 3. Functional Requirements

### 3.1 Authentication Module

#### FR-3.1.1: OAuth 2.0 Token Generation
- **Description:** System shall obtain an access token using client credentials
- **Acceptance Criteria:**
  - Successfully retrieve access token with client_id, client_secret, username, password
  - Store token locally for reuse
  - Handle token expiration time (expires_in)
  - Extract and return refresh_token for future use

#### FR-3.1.2: Token Refresh
- **Description:** System shall refresh expired tokens using refresh_token
- **Acceptance Criteria:**
  - Generate new access token using existing refresh_token
  - Update stored token information
  - Automatically refresh tokens when making API calls if expired

#### FR-3.1.3: Automatic Token Management
- **Description:** SDK shall handle token lifecycle automatically
- **Acceptance Criteria:**
  - Check token expiration before each API call
  - Automatically refresh if token is expired or about to expire
  - Handle token refresh failures gracefully

### 3.2 Store Management Module

#### FR-3.2.1: Create Store
- **Description:** Create a new store in Pathao system
- **Acceptance Criteria:**
  - Accept store details: name, contact_name, contact_number, address, etc.
  - Validate input parameters (name length 3-50, contact number length 11, etc.)
  - Return store creation confirmation with store_name
  - Handle async approval process messaging

#### FR-3.2.2: Retrieve Store Information
- **Description:** Get list of all merchant stores
- **Acceptance Criteria:**
  - Return paginated list of stores
  - Include store_id, store_name, address, status, location details
  - Support filtering and pagination
  - Handle empty store list gracefully

#### FR-3.2.3: Get Store Details
- **Description:** Retrieve details of a specific store
- **Acceptance Criteria:**
  - Accept store_id as parameter
  - Return complete store information
  - Validate store existence

### 3.3 Order Management Module

#### FR-3.3.1: Create Single Order
- **Description:** Create a new order for shipment
- **Acceptance Criteria:**
  - Accept order parameters: recipient details, delivery type, item details
  - Validate all required fields
  - Support Cash-On-Delivery (COD) orders
  - Return consignment_id and order_status
  - Return calculated delivery_fee

#### FR-3.3.2: Create Bulk Orders
- **Description:** Create multiple orders in a single request
- **Acceptance Criteria:**
  - Accept array of order objects
  - Validate each order in the batch
  - Handle partial failures gracefully
  - Return acceptance status with processing information
  - Support async processing confirmation (202 response)

#### FR-3.3.3: Get Order Information
- **Description:** Retrieve current status and details of an order
- **Acceptance Criteria:**
  - Accept consignment_id as parameter
  - Return order status, merchant_order_id, last_updated time
  - Support invoice_id retrieval
  - Validate order existence

### 3.4 Location Services Module

#### FR-3.4.1: Get Cities List
- **Description:** Retrieve all available cities for delivery
- **Acceptance Criteria:**
  - Return list of all cities with city_id and city_name
  - No authentication required for basic list

#### FR-3.4.2: Get Zones in City
- **Description:** Retrieve zones within a specific city
- **Acceptance Criteria:**
  - Accept city_id as parameter
  - Return list of zones with zone_id and zone_name
  - Validate city_id exists

#### FR-3.4.3: Get Areas in Zone
- **Description:** Retrieve areas within a specific zone
- **Acceptance Criteria:**
  - Accept zone_id as parameter
  - Return list of areas with area details
  - Include service availability flags (home_delivery_available, pickup_available)

### 3.5 Price Calculation Module

#### FR-3.5.1: Calculate Delivery Price
- **Description:** Calculate delivery price for given parameters
- **Acceptance Criteria:**
  - Accept store_id, item_type, delivery_type, item_weight, recipient location
  - Return base price, discounts, COD percentage, additional charges
  - Return final_price
  - Support different delivery types (Normal, On Demand)

### 3.6 Error Handling and Validation

#### FR-3.6.1: Input Validation
- **Description:** Validate all input parameters before API calls
- **Acceptance Criteria:**
  - Validate string lengths according to API specs
  - Validate phone number formats (11 characters)
  - Validate numeric ranges (weight: 0.5-10 kg)
  - Validate enum values (delivery_type, item_type)
  - Raise appropriate validation errors

#### FR-3.6.2: API Error Handling
- **Description:** Handle all API error responses gracefully
- **Acceptance Criteria:**
  - Catch and parse API error responses
  - Create custom exception classes for different error types
  - Provide meaningful error messages
  - Support error logging and debugging

#### FR-3.6.3: Network Error Handling
- **Description:** Handle network-related failures
- **Acceptance Criteria:**
  - Handle connection timeouts
  - Handle network unreachability
  - Support configurable retry logic
  - Implement exponential backoff for retries

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-4.1.1:** API response times should be processed within 2 seconds
- **NFR-4.1.2:** SDK should cache location data (cities, zones, areas) to reduce API calls
- **NFR-4.1.3:** Bulk order creation should support up to 1000 orders per request

### 4.2 Reliability
- **NFR-4.2.1:** SDK should have 99% successful API call rate (excluding network failures)
- **NFR-4.2.2:** Automatic token refresh should prevent authentication failures
- **NFR-4.2.3:** SDK should recover gracefully from transient failures

### 4.3 Usability
- **NFR-4.3.1:** API should follow Python best practices and PEP 8 standards
- **NFR-4.3.2:** All public methods should have comprehensive docstrings
- **NFR-4.3.3:** Type hints should be used throughout the codebase
- **NFR-4.3.4:** Error messages should be clear and actionable

### 4.4 Security
- **NFR-4.4.1:** Credentials should not be logged or exposed in error messages
- **NFR-4.4.2:** SDK should support HTTPS only
- **NFR-4.4.3:** Sensitive tokens should be handled in memory securely
- **NFR-4.4.4:** SDK should validate SSL certificates

### 4.5 Maintainability
- **NFR-4.5.1:** Code should have 80% minimum test coverage
- **NFR-4.5.2:** All complex functions should have comments explaining logic
- **NFR-4.5.3:** SDK should be version-compatible with Python 3.8+
- **NFR-4.5.4:** Dependencies should be minimal and well-maintained

### 4.6 Documentation
- **NFR-4.6.1:** Comprehensive README with quick start guide
- **NFR-4.6.2:** API reference documentation for all classes and methods
- **NFR-4.6.3:** Multiple examples for different use cases
- **NFR-4.6.4:** Contributing guidelines for open-source collaboration

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────┐
│     User Application                    │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Pathao Python SDK                     │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │  Public API Layer               │   │
│  │ (Client Class - Main Interface) │   │
│  └────────────┬────────────────────┘   │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Module Layer                    │ │
│  │ ├─ Auth Module                   │ │
│  │ ├─ Store Module                  │ │
│  │ ├─ Order Module                  │ │
│  │ ├─ Location Module               │ │
│  │ └─ Price Module                  │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  HTTP Client Layer               │ │
│  │ (Requests wrapper with retry)    │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Utilities Layer                 │ │
│  │ ├─ Validators                    │ │
│  │ ├─ Exception Classes             │ │
│  │ ├─ Data Models (Dataclasses)     │ │
│  │ └─ Logging                       │ │
│  └──────────────────────────────────┘ │
└─────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Pathao Courier API                    │
│  (Sandbox / Production)                 │
└─────────────────────────────────────────┘
```

### 5.2 Directory Structure

```
pathao-python/
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── publish.yml
├── pathao/
│   ├── __init__.py
│   ├── client.py                 # Main client class
│   ├── exceptions.py             # Custom exceptions
│   ├── models.py                 # Data models
│   ├── http_client.py            # HTTP wrapper
│   ├── validators.py             # Input validators
│   ├── logger.py                 # Logging setup
│   └── modules/
│       ├── __init__.py
│       ├── auth.py               # Authentication
│       ├── store.py              # Store operations
│       ├── order.py              # Order operations
│       ├── location.py           # Location services
│       └── price.py              # Price calculation
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_auth.py
│   ├── test_store.py
│   ├── test_order.py
│   ├── test_location.py
│   ├── test_price.py
│   ├── test_validators.py
│   └── fixtures/
│       └── mock_responses.py
├── examples/
│   ├── basic_usage.py
│   ├── create_order.py
│   ├── bulk_orders.py
│   ├── location_services.py
│   └── error_handling.py
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── authentication.md
│   ├── store_management.md
│   ├── order_management.md
│   ├── location_services.md
│   ├── price_calculation.md
│   └── error_handling.md
└── .env.example
```

---

## 6. Technical Specifications

### 6.1 Technology Stack
- **Language:** Python 3.8+
- **HTTP Client:** requests library
- **Data Serialization:** JSON
- **Testing:** pytest
- **Documentation:** MkDocs / Sphinx
- **Package Management:** pip/setuptools
- **Version Control:** Git
- **CI/CD:** GitHub Actions

### 6.2 Dependencies
- `requests>=2.28.0` - HTTP client
- `python-dotenv>=0.21.0` - Environment variable management
- `pydantic>=1.10.0` - Data validation (optional, for enhanced validation)

### 6.3 Development Dependencies
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `pytest-mock>=3.10` - Mocking utilities
- `black>=22.0` - Code formatting
- `flake8>=4.0` - Linting
- `mypy>=0.990` - Type checking
- `sphinx>=5.0` - Documentation generation

---

## 7. API Interface Specification

### 7.1 Client Initialization

```python
from pathao import PathaoClient

# Sandbox environment
client = PathaoClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_email",
    password="your_password",
    environment="sandbox"  # or "production"
)

# Or with .env file
client = PathaoClient()  # Reads from .env
```

### 7.2 Core Classes

#### PathaoClient
Main entry point for all SDK operations. Manages authentication and delegates to specific modules.

#### Module Classes
- `AuthModule` - Token management
- `StoreModule` - Store operations
- `OrderModule` - Order operations
- `LocationModule` - Location services
- `PriceModule` - Price calculation

### 7.3 Data Models (Dataclasses)

All responses should be converted to dataclass objects for type safety and ease of use.

---

## 8. Testing Strategy

### 8.1 Testing Scope
- Unit tests for all modules (target: 80% coverage)
- Integration tests for API calls (using mocks)
- Validation tests for input parameters
- Error handling tests

### 8.2 Testing Approach
- Use pytest framework
- Mock HTTP responses using unittest.mock or responses library
- Fixture-based test data
- Parametrized tests for multiple scenarios

### 8.3 Test Categories
- Authentication tests
- Store CRUD operations
- Order creation and retrieval
- Bulk order operations
- Location services
- Price calculations
- Error handling and edge cases
- Input validation

---

## 9. Release and Deployment

### 9.1 Version Strategy
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- Initial release: v0.1.0 (alpha)
- Stable release: v1.0.0

### 9.2 PyPI Publication
- Create PyPI account
- Configure setup.py/pyproject.toml
- Automated publishing via GitHub Actions
- Support for multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)

### 9.3 Documentation Hosting
- Host on ReadTheDocs or GitHub Pages
- Keep documentation in sync with releases

---

## 10. Project Milestones

### Phase 1: Core Development (Weeks 1-2)
- Project setup and configuration
- Implement authentication module
- Create data models and validators
- Set up testing infrastructure

### Phase 2: Feature Implementation (Weeks 2-4)
- Implement store management
- Implement order management
- Implement location services
- Implement price calculation

### Phase 3: Testing & Documentation (Weeks 4-5)
- Comprehensive unit and integration tests
- Write API documentation
- Create usage examples
- Performance optimization

### Phase 4: Release Preparation (Week 5-6)
- Code review and refactoring
- Final testing and QA
- Prepare for PyPI publication
- Create release notes

---

## 11. Constraints and Assumptions

### 11.1 Constraints
- Must maintain compatibility with Python 3.8+
- API rate limits may apply from Pathao
- Depends on Pathao API availability
- SSL/TLS encryption required

### 11.2 Assumptions
- Pathao API structure remains relatively stable
- Users have valid Pathao account credentials
- Internet connectivity is available for API calls
- Users have basic Python knowledge

---

## 12. Success Criteria

- [ ] All functional requirements implemented
- [ ] 80%+ test coverage achieved
- [ ] All tests passing (unit and integration)
- [ ] Code follows PEP 8 standards
- [ ] Documentation complete and reviewed
- [ ] Package successfully published on PyPI
- [ ] At least 50 downloads in first month
- [ ] No critical security vulnerabilities
- [ ] GitHub repository established with contributing guidelines
- [ ] Community feedback mechanisms in place

---

## 13. Glossary

- **Access Token:** JWT token used for authenticating API requests
- **Consignment ID:** Unique identifier for a shipment/order
- **COD:** Cash On Delivery payment method
- **OAuth 2.0:** Authorization framework for secure API access
- **Refresh Token:** Token used to obtain a new access token
- **Store ID:** Unique identifier for a merchant store
- **Zone:** Geographic subdivision within a city
- **Area:** Geographic subdivision within a zone

---

## 14. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Dev Team | Initial SRS |

---

**Document End**
