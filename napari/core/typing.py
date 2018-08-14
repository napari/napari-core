"""
Commonly used types.
"""
from typing import *
from typing import __all__
from types import ModuleType as Module

from os import PathLike

from git import RemoteProgress

__all__ += ['JSON', 'Module']


JSON = NewType('JSON', Dict)

ProgressCallback = Callable[[int, int, Optional[int], Optional[str]],
                            type(None)]
Progress = Union[RemoteProgress, ProgressCallback]
