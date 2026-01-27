# Installation Guide

## Requirements

- Python 3.8 or higher
- pip package manager

## Install from PyPI

```bash
pip install pathao
```

## Install from Source

```bash
git clone https://github.com/yourusername/pathao-python.git
cd pathao-python
pip install -e .
```

## Development Installation

```bash
git clone https://github.com/yourusername/pathao-python.git
cd pathao-python
pip install -r requirements-dev.txt
pip install -e .
```

## Verify Installation

```python
import pathao
print(pathao.__version__)

# Create a client (will fail without credentials, but verifies import)
try:
    client = pathao.PathaoClient(
        client_id="test",
        client_secret="test",
        username="test",
        password="test",
        environment="sandbox"
    )
    print("✅ Installation successful!")
except Exception as e:
    print(f"❌ Installation issue: {e}")
```

## Dependencies

The package automatically installs these dependencies:

- `requests>=2.28.0` - HTTP client
- `python-dotenv>=0.21.0` - Environment variable loading

## Environment Setup

### Option 1: Environment Variables

```bash
export PATHAO_CLIENT_ID="your_client_id"
export PATHAO_CLIENT_SECRET="your_client_secret"
export PATHAO_USERNAME="your_email"
export PATHAO_PASSWORD="your_password"
```

### Option 2: .env File

Create a `.env` file in your project root:

```env
PATHAO_CLIENT_ID=your_client_id
PATHAO_CLIENT_SECRET=your_client_secret
PATHAO_USERNAME=your_email
PATHAO_PASSWORD=your_password
```

## Next Steps

- [Authentication Guide](authentication.md)
- [Basic Usage Examples](../examples/basic_usage.py)
- [API Documentation](index.md)
