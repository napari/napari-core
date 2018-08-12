"""
Handles the loading/importing of modules into the Napari namespace.
"""
import sys
import pathlib

import importlib.abc
from importlib.util import spec_from_file_location
from importlib.machinery import ModuleSpec

from ..._internal.typing import PathLike, List, Dict, Module


class NapariPluginFinder(importlib.abc.MetaPathFinder):
    path_registry: Dict[str, PathLike] = dict()

    @staticmethod
    def get_plugin_package(plugin_name: str):
        return f'napari.plugins.{plugin_name}'

    @classmethod
    def __install__(cls):
        if cls.__installed__():
            raise RuntimeError(f'{cls} already in `sys.meta_path`!')
        sys.meta_path.append(cls)

    @classmethod
    def __uninstall__(cls):
        if not cls.__installed__():
            raise RuntimeError(f'{cls} not in `sys.meta_path`!')
        sys.meta_path.remove(cls)

    @classmethod
    def __installed__(cls):
        return cls in sys.meta_path

    @classmethod
    def find_spec(cls, fullname: str, path: PathLike = None,
                  target: Module = None):
        try:
            return spec_from_file_location(fullname,
                                           cls.path_registry[fullname])
        except KeyError:
            pass

        return None  # pass along to the next finder

    @classmethod
    def add_path(cls, plugin_name: str, abspath: PathLike):
        cls.path_registry[cls.get_plugin_package(plugin_name)] = abspath

    @classmethod
    def add_paths(cls, plugin_name: str, abspaths: List[PathLike]):
        # FIXME: dynamically generate napari.plugins.{plugin_name} parent path
        module_path = cls.get_plugin_package(plugin_name)
        module = Module(module_path)
        module.__path__ = []
        sys.modules[module_path] = module
        # END FIXME

        for path in abspaths:
            submodule = pathlib.Path(path).stem
            cls.add_path(f'{plugin_name}.{submodule}', path)
