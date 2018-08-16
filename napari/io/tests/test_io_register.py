from napari.io._register import io_registry, register, _register_one, _register


def test_register_one():
    _register_one('foo', lambda path: path)
    assert 'foo' in io_registry

def test_register_one_overwrite():
    _register_one('bar', lambda path: path)
    overwritten = _register_one('bar', lambda path: path)

    assert overwritten

def test_register():
    _register('baz', lambda path: path)
    assert 'baz' in io_registry

def test_register_multiple():
    _register(['boz', 'biz'], lambda path: path)
    assert 'boz' in io_registry
    assert 'biz' in io_registry

def test_register_multiple_overwrite():
    _register(['bis', 'bic'], lambda path: path)
    overwritten = _register(['bis', 'bic'], lambda path: path)

    assert len(overwritten) == 2

def test_register_function():
    register('bac', lambda path: path)
    assert 'bac' in io_registry

def test_register_decorator():
    @register('boc')
    def foo(path):
        return path

    assert 'boc' in io_registry
