# EasyPost Python Client Library

[![CI](https://github.com/EasyPost/easypost-python/workflows/CI/badge.svg)](https://github.com/EasyPost/easypost-python/actions?query=workflow%3ACI)
[![Coverage Status](https://coveralls.io/repos/github/EasyPost/easypost-python/badge.svg)](https://coveralls.io/github/EasyPost/easypost-python)
[![PyPI version](https://badge.fury.io/py/easypost.svg)](https://badge.fury.io/py/easypost)

EasyPost, the simple shipping solution. You can sign up for an account at <https://easypost.com>.

## Install

The library is tested against Python3 and should be compatible with PyPy3.

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

API Documentation can be found at: <https://easypost.com/docs/api>.

Upgrading major versions of this project? Refer to the [Upgrade Guide](UPGRADE_GUIDE.md).

## Development

```bash
# Install dependencies
make install

# Lint project
make lint

# Format project
make format

# Run tests
EASYPOST_TEST_API_KEY=123... EASYPOST_PROD_API_KEY=123... make test

# Run test coverage
EASYPOST_TEST_API_KEY=123... EASYPOST_PROD_API_KEY=123... make coverage

# Run security analysis
make scan

# Generate library documentation
make docs

# Update submodules
git submodule init
git submodule update --remote
```

### Testing

The test suite in this project was specifically built to produce consistent results on every run, regardless of when they run or who is running them. This project uses [VCR](https://github.com/kevin1024/vcrpy) to record and replay HTTP requests and responses via "cassettes". When the suite is run, the HTTP requests and responses for each test function will be saved to a cassette if they do not exist already and replayed from this saved file if they do, which saves the need to make live API calls on every test run. If you receive errors about a cassette expiring, delete and re-record the cassette to ensure the data is up-to-date.

**Sensitive Data:** We've made every attempt to include scrubbers for sensitive data when recording cassettes so that PII or sensitive info does not persist in version control; however, please ensure when recording or re-recording cassettes that prior to committing your changes, no PII or sensitive information gets persisted by inspecting the cassette.

**Making Changes:** If you make an addition to this project, the request/response will get recorded automatically for you if the `@pytest.mark.vcr()` decorator is included on the test function. When making changes to this project, you'll need to re-record the associated cassette to force a new live API call for that test which will then record the request/response used on the next run.

**Test Data:** The test suite has been populated with various helpful fixtures that are available for use, each completely independent from a particular user **with the exception of the USPS carrier account ID** (see [Unit Test API Keys](#unit-test-api-keys) for more information) which has a fallback value of our internal testing user's ID. Some fixtures use hard-coded dates that may need to be incremented if cassettes get re-recorded (such as reports or pickups).

#### Unit Test API Keys

The following are required on every test run:

- `EASYPOST_TEST_API_KEY`
- `EASYPOST_PROD_API_KEY`

Some tests may require an EasyPost user with a particular set of enabled features such as a `Partner` user when creating referrals. We have attempted to call out these functions in their respective docstrings. The following are required when you need to re-record cassettes for applicable tests:

- `USPS_CARRIER_ACCOUNT_ID` (eg: one-call buying a shipment for non-EasyPost employees)
- `PARTNER_USER_PROD_API_KEY` (eg: creating a referral user)
- `REFERRAL_USER_PROD_API_KEY` (eg: adding a credit card to a referral user)
