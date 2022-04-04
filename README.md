# EasyPost Python Client Library

[![CI](https://github.com/EasyPost/easypost-python/workflows/CI/badge.svg)](https://github.com/EasyPost/easypost-python/actions?query=workflow%3ACI)
[![PyPI version](https://badge.fury.io/py/easypost.svg)](https://badge.fury.io/py/easypost)

EasyPost, the simple shipping solution. You can sign up for an account at https://easypost.com.

## Install

```bash
pip install easypost
```

```python
# Import the EasyPost library:
import easypost
```

## Usage

A simple create & buy shipment example:

```python
import os
import easypost

easypost.api_key = os.getenv('EASYPOST_API_KEY')

shipment = easypost.Shipment.create(
    from_address = {
        "name": "EasyPost",
        "street1": "118 2nd Street",
        "street2": "4th Floor",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US",
        "phone": "415-456-7890",
    },
    to_address = {
        "name": "Dr. Steve Brule",
        "street1": "179 N Harbor Dr",
        "city": "Redondo Beach",
        "state": "CA",
        "zip": "90277",
        "country": "US",
        "phone": "310-808-5243",
    },
    parcel = {
        "length": 10.2,
        "width": 7.8,
        "height": 4.3,
        "weight": 21.2,
    },
)

shipment.buy(rate=shipment.lowest_rate())

print(shipment)
```

## Documentation

API Documentation can be found at: https://easypost.com/docs/api.

## Development

```bash
# Install dependencies
make install

# Lint project
make lint

# Run tests
EASYPOST_TEST_API_KEY=123... EASYPOST_PROD_API_KEY=123... make test

# Run test coverage
EASYPOST_TEST_API_KEY=123... EASYPOST_PROD_API_KEY=123... make coverage

# Get a comprehensive list of development actions
make help
```
