"""
Processing registration machinery.
"""
import inspect
from collections import namedtuple

from napari.core.lazy import LazyAttrs, lazy
from napari.core.register import Registry, register as _register

from napari.core.typing import Dict, Callable, Any


processing_registry = Registry()

fields: Dict[str, Callable[[Callable], Any]] = {
    'func': lambda func: func,
    'sig': inspect.signature,
    'doc': inspect.getdoc
}


class static(LazyAttrs):
    entry_formats = lazy(lambda: tuple(fields.items()))
    entry_type = lazy(lambda: namedtuple('ProcessingEntry',
                                         tuple(f[0] for f in
                                               static.entry_formats)))


def to_kv(callback, others):
    path, = others

    entry = dict()
    for field, func in static.entry_formats:
        entry[field] = func(callback)

    return path, static.entry_type(**entry)


def register(*args):
    """Registers an processing function. Can also be used as a decorator.

    Parameters
    ----------
    path : str
        Path under which this function will be stored.
    func : callable, optional
        Function to register.

    Returns
    -------
    func : callable
        Registered function.
    """
    return _register(processing_registry, args, to_kv=to_kv)
