from napari.io._register import (input_registry, input, _input_one, _input,
                                 output_registry, output)


def test_input_one():
    _input_one('.foo', lambda path: path)
    assert '.foo' in input_registry
    assert input_registry['.foo']('bar') == 'bar'

def test_input_one_overwrite():
    _input_one('.bar', lambda path: path)
    overwritten = _input_one('.bar', lambda path: path)

    assert overwritten

def test_input():
    _input('.baz', lambda path: path)
    assert '.baz' in input_registry

def test_input_multiple():
    _input(['.boz', '.biz'], lambda path: path)
    assert '.boz' in input_registry
    assert '.biz' in input_registry

def test_input_multiple_overwrite():
    _input(['.bis', '.bic'], lambda path: path)
    overwritten = _input(['.bis', '.bic'], lambda path: path)

    assert len(overwritten) == 2

def test_input_function():
    input('.bac', lambda path: path)
    assert '.bac' in input_registry

def test_input_decorator():
    @input('.boc')
    def foo(path):
        return path

    assert '.boc' in input_registry
    assert foo('boc') == 'boc'

def test_output():
    output('.fob', lambda path: path)
    assert '.fob' in output_registry
    assert output_registry['.fob']('bar') == 'bar'

def test_output_overwrite():
    output('.bab', lambda path: path)
    overwritten = output('.bab', lambda path: path)

    assert overwritten

def test_output_decorator():
    @output('.bob')
    def foo(path):
        return path

    assert '.bob' in output_registry
    assert foo('bob') == 'bob'
