from napari.state import State, state_registry, register_state


def test_register_state():
    class Foo(list, State):
        ...

    register_state(Foo)

    assert Foo in state_registry

def test_register_state_decorator():
    @register_state
    class Bar(dict, State):
        ...

    assert Bar in state_registry
