# setup for py.test

import datetime
import random

import easypost
import pytest


API_KEY = 'e2Cg9AScV1wqj4JuaatP7A'
PROD_API_KEY = 'vsBlV5PvQ9Yy5NZ0ieQveQ'


# this fixture is auto-loaded by all tests; it sets up the api key
@pytest.yield_fixture(autouse=True)
def setup_api_key():
    default_key = easypost.api_key
    easypost.api_key = API_KEY
    yield
    easypost.api_key = default_key


# if a test needs to use the prod api key, make it depend on this fixture
@pytest.yield_fixture()
def prod_api_key():
    default_key = easypost.api_key
    easypost.api_key = PROD_API_KEY
    yield
    easypost.api_key = default_key


@pytest.fixture
def per_run_unique():
    """Generate a string that should be very close to unique"""
    return '{0}{1}'.format(
        datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        random.randrange(1, 100)
    )
