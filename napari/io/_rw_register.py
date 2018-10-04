"""
Registration for file extension callbacks.
"""
from napari.core.typing import (RegistryDecorator, Callable, Union,
                                Dict, List, Sequence, Optional, Tuple)
from .types import ReadFileExtCallback, WriteFileExtCallback, RWCallback


def _register_one(registry: Dict[str, RWCallback],
                  filetype: str,
                  callback: RWCallback):
    registry[filetype] = callback


def _register(registry: Dict[str, RWCallback],
              filetypes: Sequence[str],
              callback: RWCallback) -> RWCallback:
    for filetype in filetypes:
        _register_one(registry, filetype, callback)
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


def _register_decorator(registry: Dict[str, RWCallback],
                        args: Sequence) -> RegistryDecorator[RWCallback]:
    if not isinstance(registry, dict):
        raise TypeError(f'expected registry {registry} '
                        f'to be dict, got {type(registry)}')

    callback, filetypes = _parse_args(args)

    if callback is not None:
        return _register(registry, filetypes, callback)

    def decorator(func):
        return _register(registry, filetypes, func)

    return decorator


read_file_ext_registry: Dict[str, ReadFileExtCallback] = dict()


def read_file_ext(*args) -> RegistryDecorator[ReadFileExtCallback]:
    """Registers a function to open files based on extension.
    Can also be used as a decorator.

    Parameters
    ----------
    filetypes : string or sequence of string
        Extension of the file(s) (including the '.').
    callback : Read_File_ExtCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of Read_File_ExtCallback or None
        Overwritten callbacks.
    """
    return _register_decorator(read_file_ext_registry, args)


write_file_ext_registry: Dict[str, WriteFileExtCallback] = dict()


def write_file_ext(*args) -> RegistryDecorator[WriteFileExtCallback]:
    """Registers a function to write files based on extension.
    Can also be used as a decorator.

    Parameters
    ----------
    filetypes : string or sequence of string
        Extension of the file(s) (including the '.').
    callback : Write_File_ExtCallback, optional
        Callback to register. If not provided, will act as a decorator.

    Returns
    -------
    overwritten : list of Write_File_ExtCallback or None
        Overwritten callbacks.
    """
    return _register_decorator(write_file_ext_registry, args)
