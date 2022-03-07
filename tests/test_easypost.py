import easypost.requestor as requestor


def test_timeout():
    assert requestor.timeout == 60

    requestor.timeout = 1

    assert requestor.timeout == 1

    requestor.timeout = 60  # Change back to 60 seconds so other tests do not timeout
