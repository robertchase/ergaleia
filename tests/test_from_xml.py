import pytest
import xml

from ergaleia.from_xml import from_xml
from ergaleia.load_from_path import load_from_path
from ergaleia.normalize_path import normalize_path


def test_empty():
    with pytest.raises(xml.sax._exceptions.SAXParseException):
        from_xml('')


@pytest.mark.parametrize('value,length,content', [
    ('<simple></simple>', 0, {}),
    ('<simple>words</simple>', 5, 'words'),
    ('<simple><a></a></simple>', 1, {'a': {}}),
    ('<simple><a>yeah</a></simple>', 1, {'a': 'yeah'}),
    ('<simple><a></a><b></b></simple>', 2, {'a': {}, 'b': {}}),
    ('<simple><a></a><b>doh</b></simple>', 2, {'a': {}, 'b': 'doh'}),
])
def test_simple(value, length, content):
    d = from_xml(value)
    c = d['simple']
    assert len(c) == length
    assert c == content


@pytest.mark.parametrize('data', [
    (load_from_path('tests.from_xml.data', 'data')),
    (open(normalize_path('tests.from_xml.data', 'data'))),
])
def test_parts(data):
    d = from_xml(data)

    d = d['PARTS']
    assert 'TITLE' in d
    assert 'PART' in d
    p = d['PART']
    assert len(p) == 4
    item = [part for part in p if part['ITEM'] == 'Motherboard'][0]
    assert item['MANUFACTURER'] == 'ASUS'
