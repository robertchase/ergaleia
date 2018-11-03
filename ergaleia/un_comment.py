'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''
import re


def un_comment(s, comment='#', strip=True):
    """Uncomment a string or list of strings

       truncate s at first occurrence of a non-escaped comment character
       remove escapes from escaped comment characters

       Parameters:
           s       - string to uncomment
           comment - comment character (default=#) (see Note 1)
           strip   - strip line after uncomment (default=True)

       Notes:
           1. Comment character can be escaped using \
           2. If a tuple or list is provided, a list of the same length will
              be returned, with each string in the list uncommented. Some
              lines may be zero length.
    """

    def _un_comment(string):
        result = re.split(r'(?<!\\)' + comment, string, maxsplit=1)[0]
        result = re.sub(r'\\' + comment, comment, result)
        if strip:
            return result.strip()
        return result

    if isinstance(s, (tuple, list)):
        return [_un_comment(line) for line in s]
    return _un_comment(s)
