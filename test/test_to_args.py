import pytest
import ergaleia.to_args as to_args


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
    args, kwargs = to_args.to_args(value)
    assert len(args) == len(args_expected)
    for a, b in zip(args, args_expected):
        assert a == b
    assert len(kwargs) == len(kwargs_expected)
    for k, v in kwargs.items():
        v == kwargs_expected[k]


@pytest.mark.parametrize('value,expected', [
    ('=', to_args.InvalidStartCharacter),
    ('a==', to_args.ConsecutiveEqual),
    ('a=b c', to_args.ExpectingKey),
    ('abc\\def', to_args.UnexpectedCharacter),
    ('abc"def', to_args.UnexpectedCharacter),
    ('abc\'def', to_args.UnexpectedCharacter),
    ('a=b c', to_args.ExpectingKey),
    ('a=b a=', to_args.DuplicateKey),
    ('a=b=', to_args.ConsecutiveKeys),
    ('a=', to_args.IncompleteKeyValue),
])
def test_to_args_errors(value, expected):
    with pytest.raises(expected):
        to_args.to_args(value)
