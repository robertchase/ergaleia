# mini

A convenient object for managing structured setting and cache data.

## description

A `Mini` object is created with a set of valid fields using
the same syntax as the `Config` constructor. All fields
exist at the top-level of the object, hence, dots `(.)` should
not be used in a field name.

#### example

```
from ergaleia import Mini

# define Mini with three fields
m = Mini('a', 'b', 'c')

# set values
m.set(a=10, b=20, c='whatever')

# use values
m.a + m.b
```

This is useful for creating a settings singleton in a module:

```
# set defaults in a module-level variable
SETTINGS = Mini('url value=https://www.example.com', 'timeout value=5')

...

# sometime later
module.SETTINGS.set(timeout=10)
```

## general operations

A `Mini` operates as a simplified, and slightly modified `Config`.

#### defining

A `Mini` is defined with a constructor using the same syntax (`definition statement`)
as a `Config`. Field names must not contain dots `(.)`.

### simple setting and getting

Access a `Mini`'s attributes with dot-notation.

```
>>> m = Mini('a value=10', b value=20')
>>> m.a
10
>>> m.a=5
>>> m.a
5
>>> m.a * m.b
100
```

#### setting with a method

The `set` method allows multiple `Mini` attributes to be set
in a single call. This might be useful during program initialization.

```
>>> m = Mini('a', 'b')
>>> m.set(a=10, b=20)
>>> m.a
10
```

#### reading values from a file

The `load` method allows attributes values to be read from a file
containing `key=value` pairs, one per line. This method is equivalent
to the `Config`'s `_load` method.


#### creating a namedtuple

The `as_tuple` method returns a `namedtuple` containing name-value pairs
for each attribute. This might be useful if you want to provide
read-only access to the contents of a `Mini`.

```
>>> m = Mini('a value=10', 'b value="yo"')
>>> m.as_tuple()
MiniConfig(a=10, b='yo')
>>> m.as_tuple('MyName')
MyName(a=10, b='yo')
```
