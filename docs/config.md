# config

A constrained-key nested-dict
for managing configuration data.

## typical use case

A `Config` object is typically used to manage configuration
data read from a set of `key=value` records in a file.
The `Config` object is used to
define and access the expected keys.

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
>>> c.foo = '30'
>>> c.foo
30
```

#### env
```
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

## other ways to define an attribute

A `Config` can also be defined by reading definition statements from
a `file` or `list` object using the `_define_from_file` method or the
`Config` constructor.

#### definition statement

A definition statement is a blank-delimited sequence
of tokens that contains elements that would normally be passed to
the `_define` method. For instance, the following call to define:
```
c._define('foo', value=10, validator=int, env='FOO')
```
can be expressed with one of these definition statements:
```
'foo' value=10 validator=int env='FOO'

foo value=10 validator=int env=FOO

foo value= 10 validator =int env = FOO

foo 10 int FOO
```

A definition statement looks like an argument list without the commas.
It also assumes that the value of a kwarg argument is `int` if it
is composed of numeric characters [0-9]; otherwise, the value is `str`.
It is only necessary to include quotes around a string if it contains
blanks.

#### using _define_from_file
```
_define_from_file(self, defn)

    Parameters:
        defn - a file path, file name, file or list

    Notes:
        1. A `file path` is a dot-separated file name that resolved
           to a file in the PYTHONPATH (See ergaleia.normalize_path).
        2. A `file name` is an os-specific name of a file in the file
           system. It will be located relative the the working
           directory of the running python program.
        3. A `file` is an object with a `readlines` method returning
           zero or more lines.
        4. `validator` can be one of int, bool or file.
```
For instance:
```
c._define_from_file([
    'server.port value=10000 validator=int',
    'server.ssl value=true, validator=bool',
])
```

#### using the Config constructor

The same set of definition statements can be passed to a `Config`
constructor:
```
c = Config([
    'server.port value=10000 validator=int',
    'server.ssl value=true, validator=bool',
])
```
