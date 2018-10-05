from napari.analysis._register import analysis_registry, register, static


def test_register_function():
    register('bac', lambda path: path)
    assert 'bac' in analysis_registry


def test_register_decorator():
    @register('boc')
    def foo(path):
        return path

    assert 'boc' in analysis_registry
    assert foo('bar') == 'bar'

    entry = analysis_registry['boc']
    for field, func in static.entry_formats:
        assert getattr(entry, field) == func(foo)
