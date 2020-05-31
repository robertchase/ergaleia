"""tests for to_arg"""
import pytest
from ergaleia import to_args


@pytest.mark.parametrize('value,args_expected,kwargs_expected', [
    ('', [], {}),
    ('a b c', ['a', 'b', 'c'], {}),
    ('a 2 "3" c', ['a', 2, '3', 'c'], {}),
    ('a    b    c', ['a', 'b', 'c'], {}),
    ('a\tb\tc', ['a', 'b', 'c'], {}),
    ('a "b c d e f" c', ['a', 'b c d e f', 'c'], {}),
    ('a "b ""c  d e f" c', ['a', 'b "c  d e f', 'c'], {}),
    ('a=b c=d', [], {'a': 'b', 'c': 'd'}),
    ('a =b c=d', [], {'a': 'b', 'c': 'd'}),
    ('a   =\tb c=d', [], {'a': 'b', 'c': 'd'}),
    ('a b c d=f g=h', ['a', 'b', 'c'], {'d': 'f', 'g': 'h'}),
    ('a b c d=f g', ['a', 'b', 'c', 'g'], {'d': 'f'}),
    (r'a\b', [r'a\b'], {}),
])
def test_to_args(value, args_expected, kwargs_expected):
    """test different inputs against expected results"""
    args, kwargs = to_args(value)
    assert len(args) == len(args_expected)
    for arg, expect in zip(args, args_expected):
        assert arg == expect
    assert len(kwargs) == len(kwargs_expected)
    for key, val in kwargs.items():
        assert val == kwargs_expected[key]


def test_numeric_value():
    """verify unquoted number values are converted to int"""
    _, kwargs = to_args("a=10 b='20'")
    assert kwargs['a'] == 10
    assert kwargs['b'] == '20'
