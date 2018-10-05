"""
Registration for file extension callbacks.
"""
from napari.core.register import Registry

from napari.core.typing import (RegistryDecorator, Callable, Union,
                                Dict, List, Sequence, Optional, Tuple)
from .types import ReadsFileExtCallback, WritesFileExtCallback, RWCallback


def _register(registry: Registry,
              filetypes: Sequence[str],
              callback: RWCallback) -> RWCallback:
    for filetype in filetypes:
        registry.register(filetype, callback)
    return callback


def _check_filetypes(filetypes: Sequence[str]):
    if len(filetypes) == 1 and filetypes[0] == '*':
        return

    for filetype in filetypes:
        if not isinstance(filetype, str):
            raise TypeError(f'filetype {filetype} must be a string; '
                            f'got {type(filetype)}')
        if not filetype.startswith('.'):
            raise ValueError(f'filetype extension {filetype}'
                             "must begin with '.'")


def _parse_args(args: Sequence) -> Tuple[RWCallback, Sequence[str]]:
    callback = None
    filetypes = ('*',)

    if args:
        if isinstance(args[0], Callable):
            if len(args) > 2:
                raise TypeError(f'arguments {args} are not of the form '
                                '(callback), '
                                '(callback, filetype), or '
                                '(callback, [filetype1, filetype2, ...])')

            callback = args[0]
            try:
                filetypes = args[1]
                if isinstance(filetypes, str):
                    filetypes = (filetypes,)
                else:
                    _check_filetypes(filetypes)
            except IndexError:
                pass
        else:
            filetypes = args
            _check_filetypes(filetypes)

    return callback, filetypes


def _register_decorator(registry: Registry,
                        args: Sequence) -> RegistryDecorator[RWCallback]:
    if not isinstance(registry, Registry):
        raise TypeError(f'expected registry {registry} '
                        f'to be Registry, got {type(registry)}')

    callback, filetypes = _parse_args(args)

    if callback is not None:
        return _register(registry, filetypes, callback)

    def decorator(func):
        return _register(registry, filetypes, func)

    return decorator


reads_file_ext_registry = Registry()


def reads_file_ext(*args) -> RegistryDecorator[ReadsFileExtCallback]:
    """Registers a function to open files based on extension.
    Can also be used as a decorator.

    Parameters
    ----------
    filetypes : string or sequence of string
        Extension of the file(s) (including the '.').
    callback : ReadsFileExtCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of ReadsFileExtCallback or None
        Overwritten callbacks.
    """
    return _register_decorator(reads_file_ext_registry, args)


writes_file_ext_registry = Registry()


def writes_file_ext(*args) -> RegistryDecorator[WritesFileExtCallback]:
    """Registers a function to write files based on extension.
    Can also be used as a decorator.

    Parameters
    ----------
    filetypes : string or sequence of string
        Extension of the file(s) (including the '.').
    callback : WritesFileExtCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of WritesFileExtCallback or None
        Overwritten callbacks.
    """
    return _register_decorator(writes_file_ext_registry, args)
