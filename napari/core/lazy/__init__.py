"""
Lazy utility functions.
"""
from ._lazy_class import lazy
from ._lazy_attrs import LazyAttrsClass, LazyAttrsObject
from ._lazy_import import LazyLoader


__all__ = ['lazy',
           'LazyAttrsClass',
           'LazyAttrsObject',
           'LazyLoader']
