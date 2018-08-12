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


class LazyAttrs(object, metaclass=LazyAttrsMeta):
    pass
