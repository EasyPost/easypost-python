import pytest

import easypost


@pytest.mark.vcr()
def test_customs_info_create(basic_customs_info):
    customs_info = easypost.CustomsInfo.create(**basic_customs_info)

    assert isinstance(customs_info, easypost.CustomsInfo)
    assert str.startswith(customs_info.id, "cstinfo_")
    assert customs_info.eel_pfc == "NOEEI 30.37(a)"


@pytest.mark.vcr()
def test_customs_info_retrieve(basic_customs_info):
    customs_info = easypost.CustomsInfo.create(**basic_customs_info)

    retrieved_customs_info = easypost.CustomsInfo.retrieve(customs_info.id)

    assert isinstance(retrieved_customs_info, easypost.CustomsInfo)
    assert retrieved_customs_info == customs_info
