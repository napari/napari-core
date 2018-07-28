"""
Utility functions for converting PyQt5 attributes.
"""
from typing import List
import re


def is_qt_class(qt_attr: str):
    return qt_attr.startswith('Q')


def is_qt_func(qt_attr: str):
    return qt_attr.startswith('q') and qt_attr[1].isupper()


def is_qt_prop(qt_attr: str, qt_module: List[str]):
    if qt_attr.startswith('set'):
        return False
    return qt_getter_to_setter(qt_attr) in qt_module


def qt_getter_to_setter(qt_attr: str):
    return f'set{qt_attr[0].capitalize()}{qt_attr[1:]}'


base_doc_link = 'http://doc.qt.io/qt-5/'


def get_class_doc(qt_class: str):
    return f'{base_doc_link}{qt_class}.html'


def get_func_doc(qt_func: str):
    return get_meth_doc('qdrawutil-h', qt_func)


def get_prop_doc(qt_class: str, qt_prop: str):
    return f'{get_meth_doc(qt_class, qt_prop)}-prop'


def get_meth_doc(qt_class: str, qt_meth: str):
    return f'{get_class_doc(qt_class)}#{qt_meth}'


# startref https://stackoverflow.com/a/1176023
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name: str):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()
# endref
