"""
IO-specific type definitions.
"""
from napari.core.typing import Callable, PathLike, Any

InputCallback = Callable[[PathLike], Any]
OutputCallback = Callable[[Any, PathLike], Any]
