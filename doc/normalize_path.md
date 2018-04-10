# normalize_path

Convert dot-separated paths to directory paths

Allows non-python files to be placed in the PYTHONPATH and be referenced
using dot-notation instead of absolute or relative file-system paths.

## usage
```
normalize_path(path, filetype=None, has_filetype=True)

    Parameters:

        path         - path to convert
        filetype     - don't include as part of path if present as last token
        has_filetype - if True, treat last dot-delimited token as filetype

    Notes:
        1. Paths are relative to PYTHONPATH.
        2. If the specified path is not a string, it is returned without
           change.
        3. If the specified path contains os-specific path separator
           characters, the path is returned without change.
        4. If has_filetype is True, filetype does not have to be specified.
           If filetype is specified, has_filetype is ignored, and filetype
           must match the last dot-delimited token exactly.
```

## example

If a text file, named `test.txt` was placed in a python repo named `myprog` in
the module named `util`, then:

`normalize_path('util.test.txt')`

would return the file-system's path to the file `test.txt`, which might
look something like:

`/home/myhome/git/myprog/util/test.txt`

*This assumes PYTHONPATH is set to `/home/myhome/git/myprog`, and the host
system uses Unix-like path names.*
