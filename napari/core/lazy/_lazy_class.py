"""
Lazy class standardization.
"""
from napari.core.typing import Callable, Any


class lazy(object):
    __slots__ = 'func_wrapper'

    def __init__(self, func_wrapper: Callable[[], Any]):
        self.func_wrapper = func_wrapper

    def resolve(self) -> Any:
        return self.func_wrapper()
