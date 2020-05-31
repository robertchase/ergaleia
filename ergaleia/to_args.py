"""
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
"""
import re


def to_args(line):
    """Tokenize line into kwargs and ordered args

         The input is a blank-delimited set of tokens, which may be grouped
         as strings (quote or double quote delimited) with embedded blanks.
         A non-string equal (=) acts as a delimiter between key-value pairs.

         Example:

             one 'two''s three' four=5 six='seven eight' nine

             parses to:

             args = ['one', "two's three", 'nine']
             kwargs = {'four': 5, 'six': 'seven eight'}

         Return:

             tuple of:
                 args as list
                 kwargs as dict

         Notes:

             1. The args and kwargs can be intermingled in any order in the
                input; the order of the args is preserved.

             2. String delimiters can appear within strings by doubling them
                up; eg: "abc""def" =>  abc"def

             3. Key-value delimiters (=) can be surrounded by blanks.

             4. Non-string integer args and kwarg values will be int; all
                other values are str.
     """

    kwargs = {}

    # extract a="b" a='b' a=b
    pats = (('"', r'(\S+)\s*=\s*"(([^"]|"")*)"(\s|$)'),
            ("'", r"(\S+)\s*=\s*'(([^']|'')*)'(\s|$)"),
            ('', r'(\S+)\s*=\s*(\S+)'))
    for delim, pat in pats:
        while True:
            res = re.search(pat, line)
            if not res:
                break
            value = res.group(2).replace(delim*2, delim)
            if not delim and value.isdigit():  # convert if unquoted number
                value = int(value)
            kwargs[res.group(1)] = value
            line = line[:res.start()] + line[res.end():]

    args = _to_args(line)

    return args, kwargs


def _to_args(line, args=None):
    """tokenize line into an ordered list of args"""

    if args is None:
        args = []

    # extract '...' "..."
    pats = (("'", r"'(([^']|'')*)'(\s|$)"),
            ('"', r'"(([^"]|"")*)"(\s|$)'))
    for delim, pat in pats:
        res = re.search(pat, line)
        if not res:
            continue
        # preserve order: _to_args(left) + match + _to_args(right)
        args.extend(_to_args(line[:res.start()]))
        value = res.group(1).replace(delim*2, delim)
        args.append(value)  # these are quoted, so no int conversion
        args.extend(_to_args(line[res.end():]))
        break

    if not args:
        # if we didn't find delimited strings, then tokenize by whitespace
        for arg in line.split():
            if arg.isdigit():
                arg = int(arg)
            args.append(arg)

    return args


if __name__ == '__main__':
    print(to_args(
        'a b"b c"c d e "and ""this""" \'b c\' d=e f g h e=1 f="abc""def"'))
