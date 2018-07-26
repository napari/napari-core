def test_import():
    from .. import testing
    testing.assert_less(0, 1)


def test_import_from():
    from ..testing import assert_almost_equal
    assert_almost_equal(1, 1.00001, 3)
