from napari.plugins.machinery._load import (get_plugin_namespace,
                                            module_name_from_filepath,
                                            create_namespace_module,
                                            make_modules_importable)


def test_get_plugin_namespace():
    assert get_plugin_namespace('foo') == 'napari.plugins.foo'

    assert get_plugin_namespace('bar.baz') == 'napari.plugins.bar.baz'


def test_module_name_from_filepath():
    assert module_name_from_filepath('foo/bar.py') == 'bar'
    assert module_name_from_filepath('foo/__init__.py') == 'foo'


def test_create_namespace_module():
    module = create_namespace_module('foo')
    assert module.__name__ == 'napari.plugins.foo'
    assert module.__path__ == []


def test_make_modules_importable():
    bar = create_namespace_module('bar')
    bar_baz = create_namespace_module('bar.baz')

    make_modules_importable([bar, bar_baz])
    from napari.plugins.bar import baz
