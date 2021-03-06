# config

A constrained-key nested-dict
for managing configuration data.

## typical use case

A `Config` object manages configuration
data read from a set of `key=value` records in a file.
The `Config` object is used to
define, load and access the expected keys.

#### example

```
from ergaleia import Config

# define config
c = Config()
c._define('server.port', value=10000, validator=int)
c._define('server.ssl', value=true, validator=config.validate_bool)

# load key=value data from file
c._load('my_config')

# use config
setup_server(port=c.server.port, is_ssl=c.server.ssl)
```

## general characteristics

The `Config` object is built as a nested dict
whose keys are constrained
to a defined structure.

#### a simple demonstration

```
>>> from ergaleia import config

>>> c = Config()

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

# load a configuration file (a list for demonstration)
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
to the `_define` method. Here is the signature of the `_define` method:

```
_define(self, name, value=None, validator=None, env=None)

Parameters:
    name      - name of the attribute
    value     - initial value of the attribute
    validator - validator callable (see Note 1)
    env       - enviromment variable for default/config override

Notes:
    1. the validator validates and optionally transforms the
       attribute:

           config.attribute = validate(new_value)

       if the validator does not throw an exception, the
       new_value is considered valid
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
a `file` or `list` object using the `_define_from_path` method or the
`Config` constructor.

#### definition statement

A definition statement is a blank-delimited sequence
of tokens that contain elements that would normally be passed to
the `_define` method. For instance, the following call to define:
```
c._define('foo', value=10, validator=int, env='FOO')
```
can be expressed with one of these equivalent definition statements:
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

Valid values for `validator` are one of int, bool or file. If
`validator` is not one of these values, it is assumed to be a
dot-delimited string which can be resolved to a function using
`import_by_path`.

#### using _define_from_path
```
_define_from_path(self, defn, filetype=None)

    Parameters:
        defn     - a file path, file name, file or list
        filetype - type component of dot-delimited path

    Notes:
        1. A 'file path' is a dot-separated file name that resolves
           to a file in the PYTHONPATH (See ergaleia.normalize_path).
        2. If 'file path' is used, the last dot-delimited token might
           represent a file-type. This can be indicated with the
           'filetype' argument.
        3. A 'file name' is an os-specific path to a file in the file
           system. It will be located relative the the working
           directory of the running python program.
        4. A 'file' is an object with a 'readlines' method returning
           zero or more lines.
```
For instance:
```
c._define_from_path([
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

The `Config` constructor takes the same arguments as the
`_define_from_path` method.

## loading values from a config file

A program using `Config` will manage the definition of valid
fields, and allow a user to adjust those values by changing
a config file.
The definitions, whether loaded from a definition file or
explicitly established with the `_define` method, are considered
code, and are not manipulated in order to configure the
operation of the program.

*A **config file** is used to configure the operation of the program.*
The default name for a `config file` is `config`, which is
the name of a
text file in the current working directory (See Note 3 below).

User settings
in a config file
are `key=value` pairs, one per line.
A `key` must match a defined config value, and a `value`
must conform to any `validation` associated with the `key`.
If a `key` has an `env` defined, and the environment variable
of that name is set, then the environment variable will
take precedence over the value read from the file.

Use the `_load` method to read in any user settings from
a file.

```
_load(self, path='config', filetype=None, relaxed=False)

    Parameters:
        path     - a file path, file name, file or list
        filetype - type component of dot-delimited path
        relaxed  - if True, define keys on the fly (see Note 5)
        ignore   - if True, ignore undefined keys in path

    Return:
        self

    Notes:
        1. A 'file path' is a dot-separated file name that resolves
           to a file in the PYTHONPATH (See ergaleia.normalize_path).
        2. If 'file path' is used, the last dot-delimited token might
           represent a file-type. This can be indicated with the
           'filetype' argument.
        3. A 'file name' is an os-specific path to a file in the file
           system. It will be located relative the the working
           directory of the running python program.
        4. A 'file' is an object with a 'readlines' method returning
           zero or more lines.
        5. Normally, keys read from the path must conform to keys
           previously defined for the Config. If the relaxed flag
           is True, any keys found in the file will be accepted.
           (The keys are automatically defined, with no `value`,
           `validator` or `env` specified). If the ignore flag is
           True, any keys found in the file that are not previously
           defined are ignored.
```

## other ways to get and set data

#### using _get

Dot or bracket notation is the typical way to access values in a `Config`.
The `_get` method allows a single-call alternative that can be useful
in certain cases. The following access calls:
```
c.a.b.c
c['a']['b']['c']
```
can also be performed with the `_get` method:
```
c._get('a.b.c')
```
If the `key`, in this case `a.b.c`, is stored in a variable,
the `_get` method allows you to directly access a value without having
to break the variable into it's component parts and loop through each access.


#### using _set

The `_load` method is the typical way to set values in a `Config`.
Dot and bracket notation are also available.
The `_set` method allows a single-call alternative that can be useful
in certain cases. The following set calls:
```
c.a.b.c = 10
c['a']['b']['c'] = 10
```
can also be performed with the `_set` method:
```
c._set('a.b.c', 10)
```

#### using _as_dict

The `_as_dict` property is a one-level dict with each
defined key in the `Config` paired with the corresponding value.
