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


@pytest.mark.parametrize('define,key,expect', [
    ('foo bar', 'foo', 'bar'),
    ('a.b 10', 'a.b', 10),
    ('10 a', '10', 'a'),
    ('10.20 a', '10.20', 'a'),
    ('10.20 30', '10.20', 30),
    ('a 1.2.3', 'a', '1.2.3'),
])
def test_get(define, key, expect):
    c = config.Config([define])
    assert c._get(key) == expect


@pytest.mark.parametrize('define,key,expect', [
    ('foo bar', 'foo', 'bar'),
    ('a.b 10', 'a.b', 10),
    ('10 a', '10', 'a'),
    ('10.20 a', '10.20', 'a'),
    ('10.20 30', '10.20', 30),
    ('a 1.2.3', 'a', '1.2.3'),
])
def test_bracket(define, key, expect):
    c = config.Config()
    c._define_from_path([define])
    access = ''.join("['{}']".format(k) for k in key.split('.'))
    access = 'c{}'.format(access)
    assert eval(access) == expect


@pytest.mark.parametrize('define,key,expect', [
    ('foo bar', 'foo', 'bar'),
    ('a.b 10', 'a.b', 10),
    ('a 1.2.3', 'a', '1.2.3'),
])
def test_dot(define, key, expect):
    c = config.Config()
    c._define_from_path([define])
    v = eval('c.{}'.format(key))
    assert v == expect


@pytest.mark.parametrize('key', [
    ('a.b.c.d',),
    ('d.e.f',),
    (10),
])
def test_get_fail(key):
    c = config.Config()
    with pytest.raises(KeyError):
        c._get(key)


def test_load_undefined():
    c = config.Config()
    with pytest.raises(KeyError):
        c._load(['a=b'])


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


def test_load_return(cfg):
    result = cfg._load(['foo=123'])
    assert isinstance(result, config.Config)
    assert result.foo == '123'


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


def test_define_from_path():
    c = config.Config()
    c._define_from_path([
        'foo value=bar',
        'bar value=10 validator=int',
        'foobar',
    ])
    assert c.foo == 'bar'
    assert c.bar == 10
    assert c.foobar is None


def double(string):
    return string + string


def test_define_from_path_dynamic():
    c = config.Config()
    c._define_from_path([
        'foo value=bar validator=tests.test_config.double',
    ])
    assert c.foo == 'barbar'
    c.foo = 'akk'
    assert c.foo == 'akkakk'


@pytest.mark.parametrize('value,expected', [
    (['foo 10', 'bar 20'], 'foo=10\nbar=20'),
    (['foo.bar 10', 'bar 20'], 'foo.bar=10\nbar=20'),
    (['foo', 'bar'], 'foo=\nbar='),
])
def test_repr(value, expected):
    cfg = config.Config(value)
    assert str(cfg) == expected


@pytest.mark.parametrize('value,expected', [
    (['foo 10', 'bar 20'], {'foo': 10, 'bar': 20}),
    (['foo.bar 10', 'bar 20'], {'foo.bar': 10, 'bar': 20}),
    (['foo', 'bar'], {'foo': None, 'bar': None}),
])
def test_as_dict(value, expected):
    cfg = config.Config(value)
    assert cfg._as_dict == expected
