# load_lines_from_file

Find and load lines from a file in pythonic ways.

## usage
```
load_lines_from_path(path, filetype=None, has_filetype=True)

    Parameters: (see normalize_path)
        path         - dot-separated path
        filetype     - optional filetype
        has_filetype - if True, treat last dot-delimited token as filetype

    Notes:
        1. If path is a file-like object, then lines are read directly
           from path, without trying to open it.
        2. Non-string paths are returned immediately (excluding the
           case in Note 1).
        3. If has_filetype is True, filetype does not have to be specified.
           If filetype is specified, has_filetype is ignored, and filetype
           must match the last dot-delimited token exactly.
```

## example

Using the file `test/load_from_path.data`, which contains:
```
one
two
three
```

```
>>> from ergaleia.load_from_path import load_lines_from_path
>>> load_lines_from_path('test.load_from_path.data')
['one\n', 'two\n', 'three\n']
```
