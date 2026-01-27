# Contributing to Pathao Python SDK

We welcome contributions to the Pathao Python SDK! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Instructions

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/pathao-python.git
   cd pathao-python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the project's style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and quality checks**
   ```bash
   # Run tests
   pytest

   # Run with coverage
   pytest --cov=pathao --cov-report=term-missing

   # Format code
   black pathao tests

   # Lint code
   flake8 pathao tests

   # Type check
   mypy pathao
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88 characters)
- Use flake8 for linting
- Include type hints for all functions and methods
- Write comprehensive docstrings using Google style

### Commit Message Format
Use conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `style:` for formatting changes
- `chore:` for maintenance tasks

### Testing Requirements
- Write tests for all new functionality
- Maintain or improve test coverage (target: 80%+)
- Use descriptive test names and docstrings
- Mock external dependencies appropriately
- Include both positive and negative test cases

### Documentation Requirements
- Update relevant documentation for new features
- Include code examples in docstrings
- Update README.md if needed
- Add entries to CHANGELOG.md

## Project Structure

```
pathao-python/
├── pathao/                 # Main package
│   ├── __init__.py        # Package initialization
│   ├── client.py          # Main client class
│   ├── exceptions.py      # Custom exceptions
│   ├── models.py          # Data models
│   ├── validators.py      # Input validation
│   ├── logger.py          # Logging utilities
│   ├── http_client.py     # HTTP client wrapper
│   └── modules/           # Service modules
│       ├── auth.py        # Authentication
│       ├── store.py       # Store management
│       ├── order.py       # Order management
│       ├── location.py    # Location services
│       └── price.py       # Price calculation
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Usage examples
└── .github/               # GitHub workflows
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pathao --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run tests with specific marker
pytest -m unit
```

### Test Categories
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **Sandbox tests**: Test against real Pathao sandbox API

### Writing Tests
- Use descriptive test class and method names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Test both success and error scenarios
- Include edge cases and boundary conditions

## Documentation

### Code Documentation
- All public classes and methods must have docstrings
- Use Google-style docstrings
- Include examples in docstrings where helpful
- Document all parameters, return values, and exceptions

### User Documentation
- Update relevant guides in `docs/` directory
- Include practical examples
- Keep documentation up-to-date with code changes

## Pull Request Process

1. **Before submitting**
   - Ensure all tests pass
   - Run code quality checks
   - Update documentation
   - Add changelog entry

2. **Pull request requirements**
   - Use the provided PR template
   - Include clear description of changes
   - Reference related issues
   - Ensure CI checks pass

3. **Review process**
   - Address reviewer feedback
   - Keep PR focused and atomic
   - Maintain clean commit history

## Issue Reporting

### Bug Reports
- Use the bug report template
- Include minimal reproduction case
- Provide environment details
- Include error messages and stack traces

### Feature Requests
- Use the feature request template
- Describe the use case clearly
- Consider backwards compatibility
- Provide implementation suggestions if possible

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Questions?

If you have questions about contributing, please:
- Check existing documentation
- Search existing issues
- Create a new issue with the question label
- Reach out to maintainers

Thank you for contributing to the Pathao Python SDK!
