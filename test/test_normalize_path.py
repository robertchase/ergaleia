import os

from ergaleia.normalize_path import normalize_path


BASE = os.path.sep.join(__file__.split(os.path.sep)[:-2])


def test_normalize_path():
    assert normalize_path('test.load_from_path.data', 'data') == \
        os.path.sep.join((BASE, 'test/load_from_path.data'))


def test_normalize_os_path():
    assert normalize_path('test/load_from_path.data', 'data') == \
        'test/load_from_path.data'


def test_normalize_non_string_path():
    assert normalize_path(['what', 'dude']) == ['what', 'dude']
