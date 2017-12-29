import pytest
import xml

from ergaleia.from_xml import from_xml


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


def test_parts():
    # --- document from comptechdoc.org
    x = '''<?xml version="1.0"?>
        <PARTS>
           <TITLE>Computer Parts</TITLE>
           <PART>
              <ITEM>Motherboard</ITEM>
              <MANUFACTURER>ASUS</MANUFACTURER>
              <MODEL>P3B-F</MODEL>
              <COST> 123.00</COST>
           </PART>
           <PART>
              <ITEM>Video Card</ITEM>
              <MANUFACTURER>ATI</MANUFACTURER>
              <MODEL>All-in-Wonder Pro</MODEL>
              <COST> 160.00</COST>
           </PART>
           <PART>
              <ITEM>Sound Card</ITEM>
              <MANUFACTURER>Creative Labs</MANUFACTURER>
              <MODEL>Sound Blaster Live</MODEL>
              <COST> 80.00</COST>
           </PART>
           <PART>
              <ITEM>23 inch Monitor</ITEM>
              <MANUFACTURER>LG Electronics</MANUFACTURER>
              <MODEL> 995E</MODEL>
              <COST> 290.00</COST>
           </PART>
        </PARTS>'''
    d = from_xml(x)

    d = d['PARTS']
    assert 'TITLE' in d
    assert 'PART' in d
    p = d['PART']
    assert len(p) == 4
    item = [part for part in p if part['ITEM'] == 'Motherboard'][0]
    assert item['MANUFACTURER'] == 'ASUS'
