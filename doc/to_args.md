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

Args and kwargs can be intermingled in any order.
The order of the args is preserved.

An arg is any sequence of non-whitespace characters.
An arg that starts with a single or double quote may contain whitespace,
and must be terminated by a matching quote.
A quoted arg may contain the quote character by
repeating (doubling) the character.

Here are some valid args:
```
a
a"a
'a'
'a b'
"a b"" c"
10
'10'
```

#### kwargs

Kwargs are composed of
a non-quoted arg-like value
followed by an equal (=)
followed by an arg-like value.
The equal may or may not be white-space delimited.

If the value is non-delimited and composed of digits,
it is converted to an int.

Here are some valid kwargs:
```
a=b
'a'=b
a='b'
a = 'c d e'
10 =20
```

#### bringing it all together
```
>>> from ergaleia import to_args
>>> args, kwargs = to_args('a b c = 10 e="20" 123')
>>> args
['a', 'b', 123]
>>> kwargs
{'c': 10, 'e', '20'}
