# import_by_path

Dynamically load a function using dotted-path notation.

## usage
```
import_by_path(path)

    Parameters:
        path - a dotted-notation path to a function

    Return:
        a callable

    Notes:
        1. The 'path' is searched relative to PYTHONPATH.
        2. If 'path' is not a string, no function lookup is
           performed.
```

## example
This example is contrived, since there is not a reason to dynamically
load `import_by_path`. This might be useful if the function `path`
is supplied by some means, like a configuration file,
such that the `path`
is not available at the time the code is written.
```
>>> from ergaleia.import_by_path import import_by_path

>>> fn = import_by_path('ergaleia.import_by_path.import_by_path')
>>> fn == import_by_path
True
```
