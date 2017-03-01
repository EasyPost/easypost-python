import easypost
import pytest

from . import constants


@pytest.yield_fixture(autouse=True)
def setup_api_key():
    default_key = easypost.api_key
    easypost.api_key = constants.API_KEY
    yield
    easypost.api_key = default_key


@pytest.yield_fixture()
def prod_api_key():
    default_key = easypost.api_key
    easypost.api_key = constants.PROD_API_KEY
    yield
    easypost.api_key = default_key
