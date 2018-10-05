from collections import namedtuple
from collections.abc import Iterable

from .typing import Callable


Entry = namedtuple('Entry', ['priority', 'key', 'value'])


def key(entry):
    return entry.priority


class Registry(Iterable):
    """Ordered registry.
    """
    __slots__ = ('_entries', '_cache')

    def __init__(self):
        self._entries = list()
        self._cache = tuple()

    def __iter__(self):
        """Iterator over the keys."""
        return iter(set(entry.key for entry in self.entries))

    def __getitem__(self, key):
        gen = self.by_key(key)
        return gen.send(None)

    def register(self, key, value, priority=0):
        """Registers a key, value pair and their priority to the registry.

        Parameters
        ----------
        key : any
            Lookup key.
        value : any
            Associated value.
        priority : any
            Comparable object to sort with.
        """
        self._entries.append(Entry(priority, key, value))
        self._cache = None

    @property
    def entries(self):
        """tuple of Entry: Registered entries.
        """
        if self._cache is None:
            self._entries.sort(key=key)
            self._cache = tuple(entry for entry in self._entries)

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


def default_to_kv(callback, others):
    return others, callback


def register(registry, args,
             get_callback=default_get_callback,
             to_kv=default_to_kv):
    callback, others = get_callback(args)

    if callback is not None:
        registry.register(*to_kv(callback, others))
        return callback

    def inner(func):
        assert isinstance(func, Callable)
        registry.register(*to_kv(func, others))
        return func

    return inner
