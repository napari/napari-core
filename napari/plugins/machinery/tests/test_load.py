from napari.plugins.machinery._load import (get_plugin_namespace,
                                            create_namespace_module,
                                            map_module_to_dict,
                                            make_module_importable,
                                            make_modules_importable)


def test_get_plugin_namespace():
    assert get_plugin_namespace('foo') == 'napari.plugins.foo'

    assert get_plugin_namespace('bar.baz') == 'napari.plugins.bar.baz'


def test_create_namespace_module():
    module = create_namespace_module('foo')
    assert module.__name__ == 'foo'
    assert module.__path__ == []


def test_map_module_to_dict():
    foo = create_namespace_module('foo')

    modules = map_module_to_dict(foo, dict())
    assert foo in modules


def test_make_module_importable():
    foo = create_namespace_module('foo')

    make_module_importable(foo)
    from napari.plugins import foo

    oof = create_namespace_module('oof')
    make_module_importable(oof)
    import napari.plugins.oof


def test_make_modules_importable():
    bar = create_namespace_module('bar')
    bar_baz = create_namespace_module('bar.baz')

    make_modules_importable([bar, bar_baz])
    from napari.plugins.bar import baz
