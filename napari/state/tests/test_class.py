from napari.state import State, DynamicState, IncompatibilityError

import pytest


def test_state_not_instantiable():
    with pytest.raises(TypeError) as e_info:
        State()

def test_dynamic_state_not_instantiable():
    with pytest.raises(TypeError) as e_info:
        DynamicState()

def test_state_register():
    State.register(dict)

    assert issubclass(dict, State)
    assert isinstance(dict(), State)
    assert isinstance({}, State)

def test_state_subclass():
    class Foo(State):
        ...

    assert issubclass(Foo, State)
    assert isinstance(Foo(), State)

def test_dynamic_state_no_register():
    with pytest.raises(NotImplementedError) as e_info:
        DynamicState.register(list)

def test_dynamic_state_subclass():
    class FooList(list, DynamicState):
        ...

    assert issubclass(FooList, DynamicState)
    assert isinstance(FooList(), DynamicState)

    assert issubclass(FooList, State)
    assert isinstance(FooList(), State)

    assert hasattr(FooList, 'extract_func')

def test_dynamic_state_extract():
    class Bar(list, DynamicState):
        ...

    @Bar.extract_func(dict)
    def extract_dict(l):
        return dict(zip(l, l))

    assert Bar([1, 2, 3]).extract_to(dict) == {1:1, 2:2, 3:3}

def test_dynamic_state_populate():
    class Baz(list, DynamicState):
        ...

    @Baz.populate_func(tuple)
    def populate_with_tuple(l, t):
        for i in t:
            l.append(i)
        return l

    assert Baz.init_with(('foo', 'bar', 'baz')) == ['foo', 'bar', 'baz']

    assert (Baz(['foo']).populate_with(('bar', 'baz', 'boz'))
            == ['foo', 'bar', 'baz', 'boz'])

def test_dynamic_state_variable_inheritance():
    class Boz(DynamicState):
        ...

    assert Boz.populates_with() == []

def test_dynamic_state_incompatibility_error():
    class Biz(DynamicState):
        ...

    with pytest.raises(IncompatibilityError):
        Biz().populate_with(None)
