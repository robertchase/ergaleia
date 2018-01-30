'''
The MIT License (MIT)

https://github.com/robertchase/ergaleia/blob/master/LICENSE.txt
'''
import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

PY3 = sys.version_info.major == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


class XmlToDict(ContentHandler):

    def __init__(self, groupby=None):
        self.data = ''
        self.stack = [(None, {})]

    def startElement(self, name, attrs):
        self.stack.append((name, {n: v for n, v in attrs.items()}))

    def endElement(self, name):
        value = self.data.strip()
        self.data = ''

        name, collection = self.stack.pop()
        p_name, p_collection = self.stack[-1]

        if not value:
            value = collection

        if name in p_collection:
            p_value = p_collection[name]
            if not isinstance(p_value, (list, tuple)):
                p_value = p_collection[name] = [p_value]
            p_value.append(value)
        else:
            p_collection[name] = value

    def characters(self, ch):
        self.data += ch if PY3 else ch.encode('ascii')


def from_xml(data, handler_class=XmlToDict):
    if isinstance(data, str):
        data = StringIO(data)
    handler = handler_class()
    p = make_parser()
    p.setContentHandler(handler)
    p.parse(data)
    return handler.stack[0][1]
