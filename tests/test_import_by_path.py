import pytest

from ergaleia import import_by_path


IMPORT = 'tests.import_by_path_data'


def test_a():
    fn = import_by_path('{}.test_a'.format(IMPORT))
    assert fn() == 'test_a'


def test__aa():
    with pytest.raises(AttributeError):
        import_by_path('{}.test_aa'.format(IMPORT))


def test_b():
    fn = import_by_path('{}.test_b'.format(IMPORT))
    assert fn(100) == 1000
