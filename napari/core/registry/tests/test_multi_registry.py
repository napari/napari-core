from .._multi_registry import MultiRegistry


def test_single():
    registry = MultiRegistry()
    register = registry.register

    register(lambda: 42, 'SPAM')
    assert 'SPAM' in registry

    @register('foo')
    def foo(bar):
        return bar

    assert registry['foo']('bar') == 'bar'


def test_multiple():
    registry = MultiRegistry()
    register = registry.register

    register(lambda: 42, ['one', 'two', 'three'])
    assert 'one' in registry
    assert 'two' in registry
    assert 'three' in registry

    @register('a', 'b', 'c')
    def foo(bar):
        return bar

    assert 'a' in registry
    assert registry['b']('baz') == 'baz'
    assert 'c' in registry
