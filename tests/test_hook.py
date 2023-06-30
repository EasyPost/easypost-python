import datetime
import uuid

import pytest


@pytest.mark.vcr()
def test_request_hooks(basic_parcel, test_client):
    def assert_request(**kwargs):
        """Make assertions about a request once the RequestHook fires."""
        assert kwargs.get("method").value == "post"
        assert kwargs.get("path") == "https://api.easypost.com/v2/parcels"
        assert "parcel" in kwargs.get("request_body")
        assert "Authorization" in kwargs.get("headers")
        assert type(kwargs.get("request_timestamp")) == datetime.datetime
        assert uuid.UUID(str(kwargs.get("request_uuid")))

    """Test that we fire a RequestHook prior to making an HTTP request."""
    test_client.subscribe_to_request_hook(assert_request)
    _ = test_client.parcel.create(**basic_parcel)


@pytest.mark.vcr()
def test_response_hooks(basic_parcel, test_client):
    def assert_response(**kwargs):
        """Make assertions about a response once the ResponseHook fires."""
        assert kwargs.get("http_status") == 201
        assert kwargs.get("method").value == "post"
        assert kwargs.get("path") == "https://api.easypost.com/v2/parcels"
        assert "object" in kwargs.get("response_body")
        assert "location" in kwargs.get("headers")
        assert kwargs.get("response_timestamp") > kwargs.get("request_timestamp")
        assert uuid.UUID(str(kwargs.get("request_uuid")))

    """Test that we fire a ResponseHook after receiving an HTTP response."""
    test_client.subscribe_to_response_hook(assert_response)
    _ = test_client.parcel.create(**basic_parcel)


@pytest.mark.vcr()
def test_unsubscribe_hooks(basic_parcel, test_client):
    """Test that we do not fire a hook once unsubscribed."""

    def fail_if_subscribed(**kwargs):
        """This function should never run since we unsubscribe from HTTP hooks."""
        raise Exception("Unsubscribing from HTTP hooks did not work as intended")

    test_client.subscribe_to_request_hook(fail_if_subscribed)
    test_client.unsubscribe_from_request_hook(fail_if_subscribed)

    test_client.subscribe_to_response_hook(fail_if_subscribed)
    test_client.unsubscribe_from_response_hook(fail_if_subscribed)

    _ = test_client.parcel.create(**basic_parcel)

    assert True
