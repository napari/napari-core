"""
Input/output registration and control hub.
"""
import os.path as _osp

from napari.core.registry import MultiRegistry, FuncInfoRegistry


def _check_filetypes(filetypes):
    if len(filetypes) == 1 and filetypes[0] == '*':
        return

    for filetype in filetypes:
        if not isinstance(filetype, str):
            raise TypeError(f'filetype {filetype} must be a string; '
                            f'got {type(filetype)}')
        if not filetype.startswith('.'):
            raise ValueError(f'filetype extension {filetype}'
                             "must begin with '.'")


reads_file_ext_registry = MultiRegistry(check_others=_check_filetypes,
                                        default=('*,'))
reads_file_ext = reads_file_ext_registry.register

writes_file_ext_registry = MultiRegistry(check_others=_check_filetypes,
                                        default=('*,'))
writes_file_ext = writes_file_ext_registry.register


io_registry = FuncInfoRegistry('IO')
register = io_registry.register

del MultiRegistry, FuncInfoRegistry


def _get_funcs(registry, ext):
    for func in registry.by_key('*'):
        yield func

    for func in registry.by_key(ext):
        yield func


def read(filepath):
    """Read a file based on its extension.

    Parameters
    ----------
    filepath : str
        File path to open.

    Returns
    -------
    data : any
        File data.
    """
    ext = _osp.splitext(filepath)[-1].lower()
    for func in _get_funcs(reads_file_ext_registry, ext):
        try:
            return func(filepath)
        except Exception:
            pass
    else:
        raise IOError(f'Could not read file {filepath} with extension {ext}')


def write(data, filepath):
    """Write a file based on its extension.

    Parameters
    ----------
    data : any
        Data to writes.
    filepath : str
        File path to writes it as.
    """
    ext = _osp.splitext(filepath)[-1].lower()
    for func in _get_funcs(writes_file_ext_registry, ext):
        try:
            return func(data, filepath)
        except Exception:
            pass
    else:
        raise IOError(f'Could not write file {filepath} with extension {ext}')
