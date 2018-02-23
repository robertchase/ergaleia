'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''
from ergaleia.normalize_path import normalize_path


def load_from_path(path, filetype=None, has_filetype=True):
    """ load file content from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and the contents are returned. (See Note 1)

        Parameters: (see normalize_path)
            path         - dot-separated path
            filetype     - optional filetype
            has_filetype - if True, treat last dot-delimited token as filetype

        Notes:
            1. If path is a file-like object, then data is read directly
               from path, without trying to open it.
            2. Non-string paths are returned immediately (excluding the
               case in Note 1).
            3. If has_filetype is True, filetype does not have to be specified.
               If filetype is specified, has_filetype is ignored, and filetype
               must match the last dot-delimited token exactly.
    """
    if not isinstance(path, str):
        try:
            return path.read()
        except AttributeError:
            return path
    path = normalize_path(path, filetype, has_filetype)
    with open(path) as data:
        return data.read()


def load_lines_from_path(path, filetype=None, has_filetype=True):
    """ load lines from a file specified as dot-separated

        The file is located according to logic in normalize_path,
        and a list of lines is returned. (See Note 1)

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
    """
    if not isinstance(path, str):
        try:
            return path.readlines()
        except AttributeError:
            return path
    path = normalize_path(path, filetype)
    with open(path) as data:
        return data.readlines()
