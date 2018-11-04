import pytest
import ergaleia.config as config


@pytest.fixture
def mini():
    return config.Mini('foo value=bar')


def test_default(mini):
    assert mini.foo == 'bar'
    with pytest.raises(TypeError):
        mini['foo']


def test_set_attribute(mini):
    mini.foo = 'whatever'
    assert mini.foo == 'whatever'
    with pytest.raises(KeyError):
        mini.bar = 'whatever'


def test_set(mini):
    mini.set(foo=1)
    assert mini.foo == 1
    with pytest.raises(KeyError):
        mini.set(bar=2)
    m = config.Mini('a', 'b', 'c')
    m.set(a=1, b=2, c=3)
    assert m.a + m.b + m.c == 6


def test_load(mini):
    mini.load(['foo=10'])
    assert mini.foo == '10'
    m = config.Mini('a validator=int')
    m.load(['a=10'])
    assert m.a == 10


def test_as_tuple(mini):
    t = mini.as_tuple()
    assert t.foo == 'bar'
