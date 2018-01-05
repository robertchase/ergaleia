import pytest
import ergaleia.config as config


@pytest.mark.parametrize('value,expected', [
    (0, False),
    (1, True),
    (True, True),
    ('true', True),
    ('TRUE', True),
    ('TrUe', True),
    (False, False),
    ('false', False),
    ('FALSE', False),
    ('FaLsE', False),
])
def test_validate_bool(value, expected):
    assert config.validate_bool(value) == expected


@pytest.mark.parametrize('value', [
    5,
    'wrong',
])
def test_validate_bool_error(value):
    with pytest.raises(ValueError):
        config.validate_bool(value)


@pytest.fixture
def cfg():
    return config.Config(['foo value=bar'])


def test_default(cfg):
    assert cfg.foo == 'bar'
    assert cfg['foo'] == 'bar'


def test_set(cfg):
    cfg._set('foo', 'whatever')
    assert cfg.foo == 'whatever'


def test_int(cfg):
    cfg._define('foo', value=0, validator=int)
    cfg._set('foo', '100')
    assert cfg.foo == 100
    with pytest.raises(ValueError):
        cfg._set('foo', 'wrong')


def test_nested_name(cfg):
    cfg._define('bar.foo', value=100)
    assert cfg.bar.foo == 100
    assert cfg['bar']['foo'] == 100


def test_load(cfg):
    cfg._load(['foo=123'])
    assert cfg.foo == '123'


def test_load_relaxed():
    cfg = config.Config()
    cfg._load(['foo=123', 'foo=234', '#foo=345'], relaxed=True)
    assert cfg.foo == '234'


@pytest.mark.parametrize('value,expected', [
    (['foo=test', '#foo=comment'], 'test'),
    (['foo=test#etc'], 'test'),
    (['foo=test\#etc'], 'test#etc'),
    (['#foo=test'], 'bar'),
    (['#foo=#test'], 'bar'),
])
def test_comment(value, expected, cfg):
    cfg._load(value)
    assert cfg.foo == expected


def test_define_from_file():
    c = config.Config()
    c._define_from_file([
        'foo value=bar',
        'bar value=10 validator=int',
        'foobar',
    ])
    assert c.foo == 'bar'
    assert c.bar == 10
    assert c.foobar is None


def test_repr(cfg):
    assert str(cfg) == 'foo=bar'
    cfg._define('akk', '100')
    assert str(cfg) == 'foo=bar\nakk=100'
    cfg._define('foo', 'something else')
    assert str(cfg) == 'foo=something else\nakk=100'
