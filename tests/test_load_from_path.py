import pytest
try:
    from StringIO import StringIO
except Exception:
    from io import StringIO

import ergaleia.load_from_path as load_from_path


@pytest.fixture
def string_file():
    return StringIO('one\ntwo')


def test_load_from_path_string(string_file):
    assert load_from_path.load_from_path(string_file) == 'one\ntwo'


def test_load_lines_from_path_string(string_file):
    assert load_from_path.load_lines_from_path(string_file) == ['one\n', 'two']


def test_load_lines_from_path_list():
    assert load_from_path.load_lines_from_path(['one', 'two']) == ['one', 'two']


def test_load_from_path_list():
    assert load_from_path.load_from_path(['one', 'two']) == ['one', 'two']


def test_load_from_path_file():
    assert load_from_path.load_from_path(
            'tests.load_from_path.data', 'data'
        ) == 'one\ntwo\nthree\n'


def test_load_lines_from_path_file():
    assert load_from_path.load_lines_from_path(
            'tests.load_from_path.data', 'data'
        ) == ['one\n', 'two\n', 'three\n']


def test_load_from_os_path():
    assert load_from_path.load_from_path(
        'tests/load_from_path.data'
    ) == 'one\ntwo\nthree\n'


def test_load_from_path_missing_file():
    with pytest.raises(IOError):
        load_from_path.load_from_path('akk')
    with pytest.raises(IOError):
        load_from_path.load_from_path('tests.akk')
    with pytest.raises(IOError):
        load_from_path.load_from_path('test/akk')
