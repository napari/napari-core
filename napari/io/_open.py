"""
Opens files based on io registry.
"""
import os.path as osp

from ._register import input_registry, output_registry
from napari.core.typing import PathLike, Any


def read(filepath: PathLike) -> Any:
    """Reads a file using the io registry.

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
    return input_registry[ext](filepath)


def write(data: Any, filepath: PathLike) -> Any:
    """Writes a file using the io registry.

    Parameters
    ----------
    data : any
        Data to write.
    filepath : str
        File path to write it as.
    """
    ext = osp.splitext(filepath)[-1]
    return output_registry[ext](data, filepath)
