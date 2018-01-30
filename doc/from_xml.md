# from_xml

Convert an `XML` document into a nested python dict.

## usage
```
from_xml(data)

    Parameters:
        data - a string or file object containing XML data

    Return:
        dict version of the data parameter
```

## example
```
>>> from ergaleia.from_xml import from_xml

>>> from_xml('<A>1</A>')
{'A': '1'}

>>> from_xml('<parent><child>fred</child><child>sally</child></parent>')
{'parent': {'child': ['fred', 'sally']}}
