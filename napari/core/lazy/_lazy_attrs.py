"""
Lazy class variable access.
"""
from ._lazy_class import lazy


class LazyAttrsMeta(type):
    def __getattribute__(cls: type, name: str):
        attr = type.__getattribute__(cls, name)

        if isinstance(attr, lazy):
            attr = attr.resolve()
            type.__setattr__(cls, name, attr)

        return attr


class LazyAttrsObject(object):
    def __getattribute__(self: object, name: str):
        attr = object.__getattribute__(self, name)

        if isinstance(attr, lazy):
            attr = attr.resolve()
            object.__setattr__(self, name, attr)

        return attr


class LazyAttrsClass(LazyAttrsObject, metaclass=LazyAttrsMeta):
    pass
