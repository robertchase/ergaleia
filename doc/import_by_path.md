# import_by_path

Dynamically load a function using dotted-path notation.

This might be useful if the function `path`
is supplied by some means, like a configuration file,
such that the `path`
is not available at the time the code is written.
## usage
```
import_by_path(path)

    Parameters:
        path - a dotted-notation path to a function

    Return:
        a callable

    Notes:
        1. The 'path' is searched relative to PYTHONPATH.
        2. If 'path' is not a string, no function lookup is performed, and
           'path' will be returned unchanged.
        3. If 'path' is incorrect a ModuleNotFoundError or
           AttributeError will be raised.
```

## example
This example is contrived, since there is not a reason to dynamically
load `import_by_path`.
```
>>> from ergaleia import import_by_path

>>> fn = import_by_path('ergaleia.import_by_path.import_by_path')
>>> fn == import_by_path
True

>>> fnp = fn('ergaleia.import_by_path.import_by_path')
>>> fnp == fn == import_by_path
True
```

## warning
It is a **horrible** idea to dynamically load code based on `path` values
from an untrusted source.

**Never** allow users to supply arbitrary values for `path`.
