import pytest
from ergaleia import to_args
from ergaleia import InvalidStartCharacter
from ergaleia import ConsecutiveEqual
from ergaleia import UnexpectedCharacter
from ergaleia import ExpectingKey
from ergaleia import DuplicateKey
from ergaleia import ConsecutiveKeys
from ergaleia import IncompleteKeyValue


@pytest.mark.parametrize('value,args_expected,kwargs_expected', [
    ('', [], {}),
    ('a b c', ['a', 'b', 'c'], {}),
    ('a    b    c', ['a', 'b', 'c'], {}),
    ('a\tb\tc', ['a', 'b', 'c'], {}),
    ('a "b c d e f" c', ['a', 'b c d e f', 'c'], {}),
    ('a "b \\"c  d e f" c', ['a', 'b "c  d e f', 'c'], {}),
    ('a=b c=d', [], {'a': 'b', 'c': 'd'}),
    ('a =b c=d', [], {'a': 'b', 'c': 'd'}),
    ('a   =\tb c=d', [], {'a': 'b', 'c': 'd'}),
    ('a b c d=f g=h', ['a', 'b', 'c'], {'d': 'f', 'g': 'h'}),
])
def test_to_args(value, args_expected, kwargs_expected):
    args, kwargs = to_args(value)
    assert len(args) == len(args_expected)
    for a, b in zip(args, args_expected):
        assert a == b
    assert len(kwargs) == len(kwargs_expected)
    for k, v in kwargs.items():
        v == kwargs_expected[k]


def test_numeric_value():
    args, kwargs = to_args("a=10 b='20'")
    assert kwargs['a'] == 10
    assert kwargs['b'] == '20'


@pytest.mark.parametrize('value,expected', [
    ('=', InvalidStartCharacter),
    ('a==', ConsecutiveEqual),
    ('a=b c', ExpectingKey),
    ('abc\\def', UnexpectedCharacter),
    ('abc"def', UnexpectedCharacter),
    ('abc\'def', UnexpectedCharacter),
    ('a=b c', ExpectingKey),
    ('a=b a=', DuplicateKey),
    ('a=b=', ConsecutiveKeys),
    ('a=', IncompleteKeyValue),
])
def test_to_args_errors(value, expected):
    with pytest.raises(expected):
        to_args(value)
