"""
IO-specific type definitions.
"""
from napari.core.typing import Callable, PathLike, Any, Union


ReadFileExtCallback = Callable[[PathLike], Any]
WriteFileExtCallback = Callable[[Any, PathLike], Any]
RWCallback = Union[ReadFileExtCallback, WriteFileExtCallback]
