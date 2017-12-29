import pytest

from ergaleia.nested_get import nested_get


@pytest.fixture
def data():
    return {'a': {'b': {'c': 10}}}


@pytest.mark.parametrize('keys,expected', [
    (('a',), {'b': {'c': 10}}),
    (('a', 'b'), {'c': 10}),
    (('a', 'b', 'c'), 10),
    (('a', 'b', 'c', 'd'), None),
])
def test_basic(data, keys, expected):
    assert nested_get(data, keys) == expected


@pytest.mark.parametrize('keys,expected', [
    (('a',), {'b': {'c': 10}}),
    (('a', 'b'), {'c': 10}),
    (('a', 'b', 'c'), 10),
    (('a', 'b', 'c', 'd'), 'hey'),
])
def test_default(data, keys, expected):
    assert nested_get(data, keys, default='hey') == expected


def test_required_keyerror(data):
    with pytest.raises(KeyError):
        assert nested_get(data, ('z',), required=True)


def test_required_typeerror(data):
    with pytest.raises(TypeError):
        assert nested_get(data, ('a', 'b', 'c', 'd'), required=True)


def test_as_list(data):
    assert nested_get(data, ('a', 'b', 'c'), as_list=True) == [10]
    assert nested_get(data, ('a', 'b'), as_list=True) == [{'c': 10}]


def test_as_list_default(data):
    assert nested_get(data, ('a', 'b', 'c', 'd'), as_list=True) == []
    assert nested_get(
        data, ('a', 'b', 'c', 'd'), default='foo', as_list=True
    ) == ['foo']
