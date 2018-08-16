"""
Main control point.
"""
import sys
from napari.core.lazy import LazyAttrs

from napari.core.typing import List, Callable, Any


def main():
    for startup_hook in entry_points.startup_hooks:
        startup_hook(sys.argv)

    ret = entry_points.blocking_application(sys.argv)

    for shutdown_hook in entry_points.shutdown_hooks:
        shutdown_hook(sys.argv)

    return ret


class entry_points(LazyAttrs):
    startup_hooks: List[Callable[[List], Any]] = []
    blocking_application: Callable[[List], Any] = lambda: None
    shutdown_hooks: List[Callable[[List], Any]] = []
