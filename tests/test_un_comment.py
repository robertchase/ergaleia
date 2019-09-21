import pytest
from ergaleia import un_comment


@pytest.mark.parametrize('value,expected', [
    ('test', 'test'),
    ('#test', ''),
    (r'\#test', '#test'),
    (r'\#te\#st', '#te#st'),
    (r'\#te#st', '#te'),
    ('te#s#t', 'te'),
    ('#te#s#t', ''),
    (r'\b\o\o', r'\b\o\o'),
    (r'\b\o#o', r'\b\o'),
    (r'\b\o\#o', r'\b\o#o'),
    (r'\b\o\##o', r'\b\o#'),
    (['a', 'b'], ['a', 'b']),
    (('a', 'b'), ['a', 'b']),
    (('a#1', '#b'), ['a', '']),
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
