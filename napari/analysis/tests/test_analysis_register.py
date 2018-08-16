from napari.analysis._register import (analysis_registry,
                                       register, fields, _register)


def test_register():
    def foo():
        return 42

    _register('foo', foo)
    foo_entry = analysis_registry['foo']

    for field in fields:
        callback = fields[field]
        assert foo_entry[field] == callback(foo)

def test_register_overwrite():
    _register('bar', lambda path: path)
    overwritten = _register('bar', lambda path: path)

    assert overwritten

def test_register_function():
    register('bac', lambda path: path)
    assert 'bac' in analysis_registry

def test_register_decorator():
    @register('boc')
    def foo(path):
        return path

    assert 'boc' in analysis_registry
    assert foo('bar') == 'bar'
