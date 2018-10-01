"""
Registration for io callbacks.
"""
from napari.core.typing import (RegistryDecorator, Callable, Union,
                                Dict, List, Sequence, Optional)
from .types import InputCallback, OutputCallback


_CALLBACK = object()

input_registry: Dict[str, InputCallback] = dict()


def _input_one(filetype: str,
               callback: Sequence[InputCallback]) -> Optional[InputCallback]:
    try:
        overwritten = input_registry[filetype]
    except KeyError:
        overwritten = None

    input_registry[filetype] = callback
    return overwritten


def _input(filetypes: Union[str, Sequence[str]],
           callback: Sequence[InputCallback]) -> Optional[List[InputCallback]]:
    if not isinstance(filetypes, Sequence) or isinstance(filetypes, str):
        filetypes = (filetypes,)
    return [_input_one(filetype, callback) for filetype in filetypes]


def input(filetypes: Union[str, Sequence[str]],
          callback: InputCallback = _CALLBACK
          ) -> Union[Optional[List[InputCallback]],
                     RegistryDecorator[InputCallback]]:
    """Registers a function to open files. Can also be used as a decorator.

    Parameters
    ----------
    filetype : string or sequence of string
        Extension of the file (including the '.') or its mimetype.
    callback : InputCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of InputCallback or None
        Overwritten callbacks.
    """
    def input_decorator(func):
        _input(filetypes, callback)
        return func

    if callback is _CALLBACK:
        return input_decorator

    return _input(filetypes, callback)


output_registry: Dict[str, OutputCallback] = dict()


def _output(filetype: str,
            callback: Sequence[OutputCallback]) -> Optional[OutputCallback]:
    try:
        overwritten = output_registry[filetype]
    except KeyError:
        overwritten = None

    output_registry[filetype] = callback
    return overwritten


def output(filetype: str,
          callback: OutputCallback = _CALLBACK
          ) -> Union[Optional[OutputCallback],
                     RegistryDecorator[OutputCallback]]:
    """Registers a function to write files. Can also be used as a decorator.

    Parameters
    ----------
    filetype : string
        File extension (including the '.') or mimetype.
    callback : OutputCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : OutputCallback or None
        Overwritten callback.
    """
    def output_decorator(func):
        _output(filetype, callback)
        return func

    if callback is _CALLBACK:
        return output_decorator

    return _output(filetype, callback)
