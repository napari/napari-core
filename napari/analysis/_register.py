"""
Processing registration machinery.
"""
import inspect

from napari.core.typing import Dict, Callable, Any


analysis_registry: Dict[str, Dict[str, Any]] = dict()

fields: Dict[str, Callable[[Callable], Any]] = {
    'func': lambda func: func,
    'sig': inspect.signature,
    'doc': inspect.getdoc
}


def _register(path: str, func: Callable):
    entry = dict()

    for field in fields:
        callback = fields[field]
        entry[field] = callback(func)

    try:
        overwritten = analysis_registry[path]
    except KeyError:
        overwritten = None

    analysis_registry[path] = entry
    return overwritten


_DECORATE = object()


def register(path: str, func: Callable = _DECORATE):
    """Registers a processing function. Can also be used as a decorator.

    Parameters
    ----------
    path : str
        Path under which this function will be stored.
    func : callable
        Function to register.

    Returns
    -------
    overwritten : dict of str: any or None
        The entry which was overwritten; if any.
    """
    def register_decorator(func: Callable):
        _register(path, func)
        return func

    if func is _DECORATE:
        return register_decorator

    return _register(path, func)
