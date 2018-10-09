from collections import namedtuple
from collections.abc import Iterable

from ..typing import Callable


Entry = namedtuple('Entry', ['priority', 'key', 'value'])


def _key(entry):
    return entry.priority


def default_get_callback(args):
    callback = None
    if len(args) == 0:
        raise TypeError()

    if isinstance(args[-1], Callable):
        callback = args[-1]
        others = args[:-1]
    else:
        others = args

    return callback, others


def default_push(add_entry, callback, others):
    add_entry(others, callback)


class Registry:
    """Ordered registry.
    """
    __slots__ = ('_entries', '_cache', '_get_callback', '_push')

    def __init__(self, get_callback=default_get_callback,
                 push=default_push, doc=None):
        self._get_callback = get_callback
        self._push = push

        if doc is not None:
            # TODO: actually change the docstring
            pass  # self.register.__doc__ = doc

        self._entries = list()
        self._cache = tuple()

    def __iter__(self):
        """Iterator over the keys."""
        return iter(set(entry.key for entry in self.entries))

    def __getitem__(self, key):
        gen = self.by_key(key)
        return gen.send(None)

    def _add_entry(self, key, value):
        """Registers a key, value pair and their priority to the registry.

        Parameters
        ----------
        key : any
            Lookup key.
        value : any
            Associated value.
        """
        # TODO: assign a priority based on plugins.yml
        priority = 0

        self._entries.append(Entry(priority, key, value))
        self._cache = None

    def register(self, *args):
        callback, others = self._get_callback(args)

        if callback is not None:
            self._push(self._add_entry, callback, others)
            return callback

        def inner(func):
            assert isinstance(func, Callable)
            self._push(self._add_entry, func, others)
            return func

        return inner

    @property
    def entries(self):
        """tuple of Entry: Registered entries.
        """
        if self._cache is None:
            self._entries.sort(key=_key)
            self._cache = tuple(self._entries)

        return self._cache

    def by_key(self, key):
        """Values grouped by key and ordered by priority.

        Parameters
        ----------
        key : any
            Lookup key.

        Yields
        ------
        value : any
            Next associated value for the key.
        """
        for entry in self.entries:
            if entry.key == key:
                yield entry.value
