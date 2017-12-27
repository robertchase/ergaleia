'''
The MIT License (MIT)

https://github.com/robertchase/tools/blob/master/LICENSE.txt
'''
from tools.normalize_path import normalize_path


def load_from_path(path, filetype=None):
    """ load file content from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and the contents are returned.

        Parameters:

            path - dot-separated path (see normalize_path)
            filetype - optional filetype (see normalize_path)
    """
    if not isinstance(path, str):
        return path
    path = normalize_path(path, filetype)
    with open(path) as data:
        return data.read()


def load_lines_from_path(path, filetype=None):
    """ load lines from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and a list of lines is returned.

        Parameters:

            path - dot-separated path (see normalize_path)
            filetype - optional filetype (see normalize_path)
    """
    if not isinstance(path, str):
        return path
    path = normalize_path(path, filetype)
    with open(path) as data:
        return data.readlines()
