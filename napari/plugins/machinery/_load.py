"""
Handles the loading and importing of plugins into the Napari namespace.
"""
import sys
import functools

from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import ModuleSpec

from napari.core.typing import PathLike, Iterable, Dict, Module, ModuleSpec


@functools.lru_cache()
def get_plugin_namespace(plugin_name: str) -> str:
    """Gets the namespace under which a plugin is importable."""
    return f'napari.plugins.{plugin_name}'


def get_plugin_spec(plugin_name: str, abs_path: PathLike) -> ModuleSpec:
    """Gets the module specification for a plugin."""
    namespace = get_plugin_namespace(plugin_name)
    spec = spec_from_file_location(namespace, location=abs_path)

    if not spec:
        raise ImportError(f"No spec found for '{plugin_name}' in {abs_path}!")

    return spec


def make_namespace_spec(plugin_name: str) -> ModuleSpec:
    """Makes a namespace spec."""
    namespace = get_plugin_namespace(plugin_name)
    return ModuleSpec(name=namespace, loader=None)


def execute_module(module: Module) -> Module:
    """Executes a module."""
    try:
        module.__loader__.exec_module(module)
    except AttributeError:
        pass

    return module


def create_namespace_module(plugin_name: str) -> Module:
    """Creates a dummy namespace module to insert into sys.modules."""
    namespace = get_plugin_namespace(plugin_name)
    module = Module(namespace)
    module.__path__ = []

    return module


def make_modules_importable(modules: Iterable[Module]) -> Dict[str, Module]:
    """Adds a list of modules to sys.modules."""
    sys.modules.update({ module.__name__: module for module in modules })
    return sys.modules
