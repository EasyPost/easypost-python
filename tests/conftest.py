# setup for py.test

import datetime
import random
import os

import easypost
import pytest


TEST_API_KEY = os.environ['TEST_API_KEY']
PROD_API_KEY = os.environ['PROD_API_KEY']


# this fixture is auto-loaded by all tests; it sets up the api key
@pytest.yield_fixture(autouse=True)
def setup_api_key():
    default_key = easypost.api_key
    easypost.api_key = TEST_API_KEY
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
    # this used to return a unique value per-run; however, now that we use
    # VCR, treat it more like an epoch
    return '20200511150500100'


@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [
            ('authorization', 'EZTK-NONE'),
            ('x-client-user-agent', 'suppressed'),
            ('user-agent', 'easypost/v2 pythonclient/suppressed'),
        ],
    }
