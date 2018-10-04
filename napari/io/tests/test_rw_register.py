from napari.io._rw_register import (_register_one, _register, _check_filetypes,
                                    _parse_args, _register_decorator)

import pytest


def test_register_one():
    registry = dict()

    _register_one(registry, '.foo', lambda path: path)
    assert '.foo' in registry
    assert registry['.foo']('bar') == 'bar'


def test_register():
    registry = dict()

    _register(registry, ('.baz',), lambda path: path)
    assert '.baz' in registry

    _register(registry, ['.boz', '.biz'], lambda path: path)
    assert '.boz' in registry
    assert '.biz' in registry


def test_check_filetypes():
    _check_filetypes(('*',))
    _check_filetypes(('.foo',))
    _check_filetypes(('.foo', '.bar', '.baz'))

    with pytest.raises(TypeError):
        _check_filetypes((1,))

    with pytest.raises(TypeError):
        _check_filetypes((1, 2, 3))

    with pytest.raises(ValueError):
        _check_filetypes(('foo',))

    with pytest.raises(ValueError):
        _check_filetypes(('foo', 'bar'))

    with pytest.raises(ValueError):
        _check_filetypes(('.foo', '*'))


def test_parse_args():
    callback, filetypes = _parse_args((lambda path: path,))
    assert callback is not None
    assert '*' in filetypes

    callback, filetypes = _parse_args((lambda path: path, '.foo'))
    assert callback is not None
    assert '.foo' in filetypes

    callback, filetypes = _parse_args((lambda path: path, ['.foo', '.bar']))
    assert callback is not None
    assert '.foo' in filetypes
    assert '.bar' in filetypes

    callback, filetypes = _parse_args(('.foo', '.bar', '.baz'))
    assert callback is None
    assert '.foo' in filetypes
    assert '.bar' in filetypes
    assert '.baz' in filetypes

    callback, filetypes = _parse_args(tuple())
    assert callback is None
    assert '*' in filetypes


def test_register_decorator():
    registry = dict()

    def register(*args):
        return _register_decorator(registry, args)

    register(lambda path: path)
    assert '*' in registry

    register(lambda path: path, '.foo')
    assert '.foo' in registry

    register(lambda path: path, ['.bar', '.baz'])
    assert '.bar' in registry
    assert '.baz' in registry

    registry.pop('*')

    @register
    def foo(path):
        return path

    assert foo('foo') == 'foo'
    assert registry['*'] is foo

    @register('.boc')
    def bar(path):
        return path

    assert bar('bar') == 'bar'
    assert registry['.boc'] is bar

    @register('.bor', '.boz')
    def baz(path):
        return path

    assert baz('baz') == 'baz'
    assert registry['.bor'] is baz
    assert registry['.boz'] is baz
