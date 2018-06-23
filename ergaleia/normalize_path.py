'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''
import os
import sys

PY3 = sys.version[0] == '3'

if PY3:
    import importlib.util
else:
    import imp


def normalize_path(path, filetype=None, has_filetype=True):
    """ Convert dot-separated paths to directory paths

    Allows non-python files to be placed in the PYTHONPATH and be referenced
    using dot-notation instead of absolute or relative file-system paths.

    If a text file, named test.txt was placed in a python repo named myprog in
    the module named util, then:

        normalize_path('myprog.util.test.txt')

    would return the file-system's path to the file 'test.txt'.

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
    """
    if not isinstance(path, str):
        return path
    if '.' in path and os.path.sep not in path:  # path is dot separated
        parts = path.split('.')
        extension = ''
        if len(parts) > 1:
            if filetype and has_filetype:
                has_filetype = False  # filetype is more specific
            if (filetype and parts[-1] == filetype) or has_filetype:
                extension = '.' + parts[-1]
                parts = parts[:-1]
            if len(parts) > 1:
                if PY3:
                    spec = importlib.util.find_spec(parts[0])
                    path = list(spec.submodule_search_locations)[0]
                else:
                    _, path, _ = imp.find_module(parts[0])

                path = os.path.join(path, *parts[1:]) + extension
    return path
