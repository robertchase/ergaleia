'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''


def nested_get(d, keys, default=None, required=False, as_list=False):
    """ Multi-level dict get helper

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
    """
    if isinstance(keys, str):
        keys = keys.split('.')
    for key in keys:
        try:
            d = d[key]
        except KeyError:
            if required:
                raise
            d = default
            break
        except TypeError:
            if required:
                raise
            d = default
            break
    if as_list:
        return [] if d is None else [d] if not isinstance(d, list) else d
    return d
