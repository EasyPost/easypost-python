import easypost
import re


def test_version_makes_sense():
    assert re.match(r'^([0-9]+\.)*[0-9]$', easypost.__version__)
    assert isinstance(easypost.version_info, tuple)
    assert all(isinstance(part, int) for part in easypost.version_info)


def test_author_makes_sense():
    assert re.match(r'.* \<\w+@easypost\.com\>$', easypost.__author__)
