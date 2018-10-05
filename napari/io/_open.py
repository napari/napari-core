"""
Opens files based on io registry.
"""
import os.path as osp

from ._rw_register import reads_file_ext_registry, writes_file_ext_registry
from napari.core.typing import PathLike, Any


def _get_funcs(registry, ext):
    for func in registry.by_key('*'):
        yield func

    for func in registry.by_key(ext):
        yield func


def read(filepath: PathLike) -> Any:
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
    ext = osp.splitext(filepath)[-1]
    for func in _get_funcs(reads_file_ext_registry, ext):
        try:
            return func(filepath)
        except Exception:
            pass


def write(data: Any, filepath: PathLike) -> Any:
    """Write a file based on its extension.

    Parameters
    ----------
    data : any
        Data to writes.
    filepath : str
        File path to writes it as.
    """
    ext = osp.splitext(filepath)[-1]
    for func in _get_funcs(writes_file_ext_registry, ext):
        try:
            return func(data, filepath)
        except Exception:
            pass
