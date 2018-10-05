"""
IO-specific type definitions.
"""
from napari.core.typing import Callable, PathLike, Any, Union


ReadsFileExtCallback = Callable[[PathLike], Any]
WritesFileExtCallback = Callable[[Any, PathLike], Any]
RWCallback = Union[ReadsFileExtCallback, WritesFileExtCallback]
