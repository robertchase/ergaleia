import os
import pytest

from ergaleia.normalize_path import normalize_path


BASE = os.path.sep.join(__file__.split(os.path.sep)[:-2])


@pytest.mark.parametrize('path,filetype,has_filetype,expected', [
    ('tests.b.c.d', None, True, 'tests/b/c.d'),
])
def test_normalize_path(path, filetype, has_filetype, expected):
    assert normalize_path(path, filetype, has_filetype) == \
        os.path.sep.join((BASE, expected))


def test_normalize_path_with_filetype():
    assert normalize_path('tests.load_from_path.data', 'data') == \
        os.path.sep.join((BASE, 'tests/load_from_path.data'))


def test_normalize_os_path():
    assert normalize_path('tests/load_from_path.data', 'data') == \
        'tests/load_from_path.data'


def test_normalize_non_string_path():
    assert normalize_path(['what', 'dude']) == ['what', 'dude']
