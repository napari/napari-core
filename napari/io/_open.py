"""
Opens files based on io registry.
"""
import os.path as osp

from ._rw_register import read_file_ext_registry, write_file_ext_registry
from napari.core.typing import PathLike, Any


def read(filepath: PathLike) -> Any:
    """Reads a file based on its extension.

    Parameters
    ----------
    filepath : str
        File path to open.

    Returns
    -------
    data : any
        File data.
    """
    try:
        return read_file_ext_registry['*'](filepath)
    except Exception:
        pass

    ext = osp.splitext(filepath)[-1]
    return read_file_ext_registry[ext](filepath)


def write(data: Any, filepath: PathLike) -> Any:
    """Writes a file based on its extension.

    Parameters
    ----------
    data : any
        Data to write.
    filepath : str
        File path to write it as.
    """
    try:
        return write_file_ext_registry['*'](filepath)
    except Exception:
        pass

    ext = osp.splitext(filepath)[-1]
    return write_file_ext_registry[ext](data, filepath)
