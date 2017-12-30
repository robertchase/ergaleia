import pytest
from ergaleia.un_comment import un_comment


@pytest.mark.parametrize('value,expected', [
    ('test', 'test'),
    ('#test', ''),
    ('\#test', '#test'),
    ('\#te\#st', '#te#st'),
    ('\#te#st', '#te'),
    ('te#s#t', 'te'),
    ('#te#s#t', ''),
    ('\b\o\o', '\b\o\o'),
    ('\b\o#o', '\b\o'),
    ('\b\o\#o', '\b\o#o'),
    ('\b\o\##o', '\b\o#'),
])
def test_un_comment(value, expected):
    assert un_comment(value) == expected


@pytest.mark.parametrize('value,strip,expected', [
    ('test', True, 'test'),
    ('test', False, 'test'),
    (' test  ', True, 'test'),
    (' test  ', False, ' test  '),
    (' te  #  st  ', True, 'te'),
    (' te  #  st  ', False, ' te  '),
])
def test_un_comment_strip(value, strip, expected):
    assert un_comment(value, strip=strip) == expected
