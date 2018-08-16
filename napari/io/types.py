"""
IO-specific type definitions.
"""
from napari.core.typing import Callable, PathLike
from napari.state import State


IOCallback = Callable[[PathLike], State]
