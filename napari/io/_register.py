"""
Registration for io callbacks.
"""
from napari.core.typing import (RegistryDecorator, Callable, Union,
                                Dict, List, Iterable, Optional)
from .types import IOCallback


io_registry: Dict[str, IOCallback] = dict()


def _register_one(filetype: str,
                  callback: Iterable[IOCallback]) -> Optional[IOCallback]:
    try:
        overwritten = io_registry[filetype]
    except KeyError:
        overwritten = None

    io_registry[filetype] = callback
    return overwritten


def _register(filetypes: Union[str, Iterable[str]],
              callback: Iterable[IOCallback]) -> Optional[List[IOCallback]]:
    if not isinstance(filetypes, Iterable) or isinstance(filetypes, str):
        filetypes = (filetypes,)
    return [_register_one(filetype, callback) for filetype in filetypes]


_CALLBACK = object()


def register(filetypes: Union[str, Iterable[str]],
             callback: IOCallback = _CALLBACK
             ) -> Union[Optional[List[IOCallback]],
                        RegistryDecorator[IOCallback]]:
    """Registers a function to open files. Can also be used as a decorator.

    Parameters
    ----------
    filetype : string or sequence of string
        Extension of the file or its mimetype.
    callback : IOCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of IOCallback or None
        Overwritten callbacks.
    """
    def register_decorator(func: IOCallback):
        _register(filetypes, callback)
        return func

    if callback is _CALLBACK:
        return register_decorator

    return _register(filetypes, callback)
