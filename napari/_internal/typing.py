"""Commonly used types.
"""
from typing import *
from typing import __all__

__all__ += ['JSON']


JSON = NewType('JSON', Union[List, Dict])

ProgressCallback = Callable[[int, int, Optional[int], Optional[str]], type(None)]
import git
Progress = Union[git.RemoteProgress, ProgressCallback]
