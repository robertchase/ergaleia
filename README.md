# ergaleia

## a library of tools for python

`Ergaleia` is a library of random tools that might be useful when writing stuff in `python`.

I found myself copying most of these things around from repo to repo, making small tweaks along the way
and letting things slowly drift out of sync. That was a bad idea.
I thought about making a bunch of individual repos, one for each tool,
but didn't like that either.
So here they are, thrown together. Maybe you'll find this useful.

You can borrow and steal if you want, just keep the license intact.

## compatability

Tested with 2.7 and 3.6.

# the tools

## config

A pythonic configuration object that reads `key=value` settings from a text file.
The text file is constrained to a set of valid keys, which can have
default values if not present in a config file.

[config documentation](doc/config.md)

## from_xml

A conversion tool to turn an `XML` document into a nested python dict.
So, why did *they* invent `XML` again?


[from_xml documentation](doc/from_xml.md)

## import_by_path

A function loader that locates and dynamically loads functions using dotted-path notation.

[import_by_path documentation](doc/import_by_path.md)

## load_from_path

A pair of file loader functions that can find, and load, files in pythonic ways.

This is a file-loader on top of `normalize_path`.

[load_from_path documentation](doc/load_from_path.md)

[load_lines_from_path documentation](doc/load_lines_from_path.md)

## nested_get

Index deep python dict structures in a single bound.

Sometimes,
like when `XML` documents are converted into python dicts (cough, cough),
data structures can end up being uncomfortably deep.
The `nested_get` function allows safe deep-traversal with default values
and optionally required structure.

[nested_get documentation](doc/nested_get.md)

## normalize_path

Find non-python files buried in the python directories using dot-notation instead
of direct file references. Useful for data or configuration files.

[normalize_path documentation](doc/normalize_path.md)

## un_comment

Truncate a string at a comment character. Handles escaped characters and
whitespace stripping.

[un_comment documentation](doc/un_comment.md)

## to_args

Parse a string into args and kwargs. Might be useful for mini-languages or
configuration tasks.

[to_args documentation](doc/to_args.md)
