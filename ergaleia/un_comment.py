'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''


def un_comment(s, comment='#', strip=True):
    """ uncomment a string

        truncate s at first occurrence of a non-escaped comment character
        remove escapes from escaped comment characters

        Parameters:
            s       - string to uncomment
            comment - comment character (default=#) (see Note 1)
            strip   - strip line after uncomment (default=True)

        Notes:
            1. Comment character can be escaped using \.
            2. Don't use when speed is important.
    """
    escape = '\\'
    is_escape = False
    result = ''
    for c in s:
        if c == comment:
            if is_escape:
                is_escape = False
            else:
                break
        if is_escape:
            result += escape
        if c == escape:
            is_escape = True
        else:
            is_escape = False
            result += c
    if strip:
        result = result.strip()
    return result
