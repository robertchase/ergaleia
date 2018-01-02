# config

A constrained-key nested-dict
for managing configuration data.

## typical use case

A `Config` object is typically used to manage configuration
data read from set of `key=value` records in a file.
The `Config` object is used to
define expected keys
and set default values.

#### example

```
import ergaleia.config as config

# define config
c = config.Config()
c._define('server.port', value=10000, validator=int)
c._define('server.ssl', value=true, validator=config.validate_bool)

# load data from file
c._load('my_config)

# use config
setup_server(port=c.server.port, is_ssl=c.server.ssl)
```

## general characteristics

The `Config` object is built as a nested dict
whose keys are constrained
to a defined structure.

#### a simple demonstration

```
>>> import ergaleia.config as config

>>> c = config.Config()

# try to access an attribute
>>> c.foo
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ergaleia/config.py", line 16, in __getattr__
    attr = self.__lookup(name)
  File "ergaleia/config.py", line 12, in __lookup
    raise KeyError(name)
KeyError: 'foo'

# define an attribute with a default value
>>> c._define('foo', 'bar')

# and access it again
>>> c.foo
'bar'

# load a configuration file (a list for simplicity)
>>> c._load(['foo=rab'])

# and take a look
>>> c.foo
'rab'
>>> c['foo']
'rab'
```

This example demonstrates several characteristics of a `Config`:

* only *defined* attributes can be accessed

* attribute values can be loaded from a file

* attributes can be accessed with `dot` or `bracket` notation

## defining an attribute

An attribute can be defined in the `Config` constructor, or by making a call
to the `_define` method. We'll start with the `_define` method:

```
_define(self, name, value=None, validator=None, env=None)

Parameters:
    name      - name of the attribute
    value     - initial value of the attribute
    validator - validator callable
    env       - enviromment variable for default/config override
```

#### simple attribute
```
>>> c._define('foo')
>>> print(c.foo)
None
>>> c.foo = 1
>>> c.foo
1
>>> c['foo']
1
```

#### nested attribute
```
>>> c._define('a.b')
>>> print(c.a.b)
None
>>> c.a.b = 'hello'
>>> c.a.b
'hello'
>>> c['a']['b']
'hello'

# kinda weirdly...
>>> c['a'].b
'hello'
>>> c.a['b']
'hello'
```

#### set a default value
```
>>> c._define('foo', value=10)
>>> c.foo
10
```

#### enforce an type
```
>>> c._define('foo', value=10, validator=int)
>>> c.foo = 'bar'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ergaleia/config.py", line 28, in __setattr__
    attr.value = value
  File "ergaleia/config.py", line 176, in __setattr__
    value = validator(value)
  File "ergaleia/config.py", line 196, in validate_int
    return int(value)
ValueError: invalid literal for int() with base 10: 'bar'
>>> c.foo = 20
>>> c.foo
20
```

#### env
````
>>> import os
>>> os.environ['FOO'] = 1234
>>> c._define('foo', 10, int, 'FOO')

# env wins over default
>>> c.foo
1234

# env wins over config file
>>> c._load(['foo=100'])
>>> c.foo
1234

# but directly setting always wins
>>> c.foo = 100
>>> c.foo
100
>>> c['foo'] = 200
>>> c.foo
200
```
