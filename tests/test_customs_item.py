import pytest

import easypost


@pytest.mark.vcr()
def test_customs_item_create(basic_customs_item):
    customs_item = easypost.CustomsItem.create(**basic_customs_item)

    assert isinstance(customs_item, easypost.CustomsItem)
    assert str.startswith(customs_item.id, "cstitem_")
    assert customs_item.value == "23.25"


@pytest.mark.vcr()
def test_customs_item_retrieve(basic_customs_item):
    customs_item = easypost.CustomsItem.create(**basic_customs_item)

    retrieved_customs_item = easypost.CustomsItem.retrieve(customs_item.id)

    assert isinstance(retrieved_customs_item, easypost.CustomsItem)
    assert retrieved_customs_item == customs_item
