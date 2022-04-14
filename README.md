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

Upgrading major versions of this project? Refer to the [Upgrade Guide](UPGRADE_GUIDE.md).

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

### Testing

The test suite in this project was specifically built to produce consistent results on every run, regardless of when they run or who is running them. This project uses [VCR](https://github.com/kevin1024/vcrpy) to record and replay HTTP requests and responses via "cassettes". When the suite is run, the HTTP requests and responses for each test function will be saved to a cassette if they do not exist already and replayed from this saved file if they do, which saves the need to make live API calls on every test run.

If you make an addition to this project, the request/response will get recorded automatically for you if the `@pytest.mark.vcr()` decorator is included on the test function. When making changes to this project, you'll need to re-record the associated cassette to force a new live API call for that test which will then record the request/response used on the next run.

The test suite has been populated with various helpful fixtures that are available for use, each completely independent from a particular user **with the exception of the USPS carrier account ID** which has a fallback value to our internal testing user's ID. If you are a non-EasyPost employee and are re-recording cassettes, you may need to provide the `USPS_CARRIER_ACCOUNT_ID` environment variable with the ID associated with your USPS account (which will be associated with your API keys in use) for tests that use this fixture.

**Note on dates:** Some fixtures use hard-coded dates that may need to be incremented if cassettes get re-recorded (such as reports or pickups).
