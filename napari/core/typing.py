"""
Commonly used types.
"""
import typing as typ
from typing import *

from types import ModuleType as Module
from os import PathLike
from git import RemoteProgress

__all__ = typ.__all__ + ['JSON', 'Module', 'RegistryDecorator']


JSON = NewType('JSON', Dict)

ProgressCallback = Callable[[int, int, Optional[int], Optional[str]],
                            type(None)]
Progress = Union[RemoteProgress, ProgressCallback]


class _RegistryDecorator:
    """Registry decorator type.

    RegistryDecorator[X] is equivalent to Callable[[X], X]
    where X is a Callable.
    """
    __slots__ = ()

    @typ._tp_cache
    def __getitem__(self, callable_type: Callable) -> Callable:
        return Callable[[callable_type], callable_type]


RegistryDecorator = _RegistryDecorator()
