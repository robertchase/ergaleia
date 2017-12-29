'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''
from ergaleia.normalize_path import normalize_path


def load_from_path(path, filetype=None):
    """ load file content from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and the contents are returned. (See Note 1)

        Parameters:

            path - dot-separated path (see normalize_path)
            filetype - optional filetype (see normalize_path)

        Notes:
            1. If path is a file-like object, then data is read directly
               from path, without trying to open it.
            2. Non-string paths are returned immediately (excluding the
               case in Note 1).
    """
    if not isinstance(path, str):
        if hasattr(path, 'read'):
            return path.read()
        return path
    path = normalize_path(path, filetype)
    with open(path) as data:
        return data.read()


def load_lines_from_path(path, filetype=None):
    """ load lines from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and a list of lines is returned. (See Note 1)

        Parameters:

            path - dot-separated path (see normalize_path)
            filetype - optional filetype (see normalize_path)

        Notes:
            1. If path is a file-like object, then data is read directly
               from path, without trying to open it.
            2. Non-string paths are returned immediately (excluding the
               case in Note 1).
    """
    if not isinstance(path, str):
        if hasattr(path, 'readlines'):
            return path.readlines()
        return path
    path = normalize_path(path, filetype)
    with open(path) as data:
        return data.readlines()
