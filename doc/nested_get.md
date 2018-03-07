# nested_get

More easily traverse deeply-nested dicts

Sometimes converted `XML` or `json` structures can end up as
difficult-to-navigate dicts. This function makes it easy
to deal with these structures by allowing for easier
expression of the navigation and default actions on
missing structure.

## signature
```
nested_get(d, keys, default=None, required=False, as_list=False)

Parameters:
    d        - dict instance
    keys     - iterable of keys or dot-delimited str of keys (see
               Note 1)
    default  - value if index fails
    required - require every index to work (see Note 2)
    as_list  - return result as list (see Note 3)

Notes:
    1. Each key is used to index a dict, replacing the dict with
       the matching value. This process is repeated until an index
       fails, or the keys are exhausted.

       If keys is a string, it is split by '.' and treated as a
       list of keys.
    2. If the required flag is False, a failure to match a key
       causes the default value to be used. If the required flag is
       True, every key must match, otherwise a TypeError or KeyError is
       raised.
    3. If as_list is True, a non-list match will be wrapped in a list,
       unless match is None, which will be replaced with an empty list.
```
 ## example
```
>>> from ergaleia.nested_get import nested_get
>>> d = {'a':{'b':{'c':1}}}
>>> d
{'a': {'b': {'c': 1}}}
>>> nested_get(d, ('a','b','c'))
1
>>> nested_get(d, ('a.b.c'))
1
>>> nested_get(d, ('a','b','d'))
>>>
>>> nested_get(d, ('a','b','d'), default='0')
>>> 0
>>> nested_get(d, ('a','b','d'), required=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ergaleia/nested_get.py", line 30, in nested_get
    d = d[key]
KeyError: 'd'
>>> nested_get(d, ('a','b','c'), as_list=True)
>>> [1]
>>> nested_get(d, ('a','b','c'), as_list=True)
>>> []
```
