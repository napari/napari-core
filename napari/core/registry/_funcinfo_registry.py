import inspect
from collections import namedtuple

from ._registry import Registry
from napari.core.lazy import LazyAttrsObject, lazy


doc = """Registers a{} {} function. Can also be used as a decorator.

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


class FuncInfoRegistry(Registry, LazyAttrsObject):
    __slots__ = ('_entry_formats', '_entry_type', 'fields')

    def __init__(self, name='FuncInfo'):
        docname = name.lower()
        super().__init__(push=self._funcinfo_push,
                         doc=doc.format('n' if docname[0] in 'aeiou' else '',
                                        docname))

        self.fields = dict(func=lambda func: func,
                           sig=inspect.signature,
                           doc=inspect.getdoc)

        self._entry_formats = lazy(lambda: tuple(self.fields.items()))
        self._entry_type = lazy(lambda: namedtuple(f'{name}Entry',
                                                   tuple(f for f, c in
                                                         self._entry_formats)))

    def _funcinfo_push(self, add_entry, callback, others):
        path, = others

        entry = dict()
        for field, func in self._entry_formats:
            entry[field] = func(callback)

        add_entry(path, self._entry_type(**entry))
