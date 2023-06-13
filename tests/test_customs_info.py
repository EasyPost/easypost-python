import pytest
from easypost.models import CustomsInfo


@pytest.mark.vcr()
def test_customs_info_create(basic_customs_info, test_client):
    customs_info = test_client.customs_info.create(**basic_customs_info)

    assert isinstance(customs_info, CustomsInfo)
    assert str.startswith(customs_info.id, "cstinfo_")
    assert customs_info.eel_pfc == "NOEEI 30.37(a)"


@pytest.mark.vcr()
def test_customs_info_retrieve(basic_customs_info, test_client):
    customs_info = test_client.customs_info.create(**basic_customs_info)

    retrieved_customs_info = test_client.customs_info.retrieve(customs_info.id)

    assert isinstance(retrieved_customs_info, CustomsInfo)
    assert retrieved_customs_info == customs_info
