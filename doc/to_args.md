# to_args

Parse a string into args and kwargs.

This may be useful for configuration or mini-language support.

The string is a blank-delimited set of tokens.
There are zero or more `args` tokens
followed by zero or more `kwargs`.
This follows the argument pattern of a python function call,
without the commas.


## components of the string

#### args

Args come first in the string, followed by kwargs. Once the switch
is made to kwargs, args are no longer accepted.

An arg is any sequence of non-whitespace characters. If an arg contains
a single (') or double (") quote, it must be preceeded by an escape (\\).
An arg that starts with a single or double quote may contain whitespace,
and must be terminated by a matching quote.

Here are some valid args:
```
a
'a'
'a b'
"a b\" c"
10
'10'
```

#### kwargs

Kwargs are composed of two arg-like values with an equal (=) in between.
The equal may or may not be white-space delimited.

Here are some valid kwargs:
```
a=b
'a'=b
a='b'
"a b" = 'c d e'
10 =20
```

#### bringing it all together
```
>>> from ergaleia.to_args import to_args
>>> args, kwargs = to_args('a b 123 "c d"=10 e="20"')
>>> args
['a', 'b', 123]
>>> kwargs
{'c d': 10, 'e', '20'}
