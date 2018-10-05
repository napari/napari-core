from napari.processing._register import processing_registry, register, static


def test_register_function():
    register('bac', lambda path: path)
    assert 'bac' in processing_registry

def test_register_decorator():
    @register('boc')
    def foo(path):
        return path

    assert 'boc' in processing_registry
    assert foo('bar') == 'bar'

    entry = processing_registry['boc']
    for field, func in static.entry_formats:
        assert getattr(entry, field) == func(foo)
