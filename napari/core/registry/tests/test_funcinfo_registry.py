from .._funcinfo_registry import FuncInfoRegistry


def test_register():
    registry = FuncInfoRegistry()
    register = registry.register

    register('foo', lambda: 42)
    register('foo.bar', lambda x: x)
    register('foo.bar.baz', lambda x, y: x + y)

    @register('foo.bar.baz.boz')
    def foo():
        print('SPAM')

    assert 'foo' in registry
    assert 'foo.bar' in registry
    assert 'foo.bar.baz' in registry
    assert 'foo.bar.baz.boz' in registry


def test_change_fields():
    registry = FuncInfoRegistry()
    register = registry.register

    registry.fields['spam'] = lambda func: 'SPAM' + func.__name__

    @register('foo')
    def foo():
        return 42

    entry = registry['foo']
    for field, func in registry._entry_formats:
        assert getattr(entry, field) == func(foo)

    registry.fields['eggs'] = lambda func: 'aliiiens'
    for field, func in registry._entry_formats:
        assert field != 'eggs'
