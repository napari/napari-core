"""
Manages plugins.
"""
import os.path as osp

from ._config import (load_plugins_spec, save_plugins_spec,
                      load_napari_spec, install_specs_from_plugins_spec,
                      normalize_crossplatform_path,
                      get_abs_plugin_path, napari_spec_from_install_spec,
                      package_spec_from_napari_spec, entry_points as cep)
from ._git import get_repo, update_plugin_from_remote
from ._load import (get_plugin_spec, module_from_spec, execute_module,
                    create_namespace_module, make_modules_importable)

from napari.core.lazy import lazy, LazyAttrs
from napari.core.typing import JSON, Module, List


def update_plugin(install_spec: JSON):
    """Updates a plugin given its specification."""
    if install_spec.get('development'):
        return

    try:
        repo = get_repo(install_spec)
        remote = install_spec['git_source']
        version = install_spec.get('version')

        update_plugin_from_remote(repo, remote, version)
    except KeyError:
        pass


def find_modules(install_spec: JSON) -> List[Module]:
    """Loads a module given its napari specification."""
    napari_spec = napari_spec_from_install_spec(install_spec)
    package_spec = package_spec_from_napari_spec(napari_spec)

    plugin_name = package_spec['plugin_name']

    base_path = osp.join(cep.plugins_path,
                         get_abs_plugin_path(install_spec))

    try:
        path = normalize_crossplatform_path(package_spec['path'])
        spec = get_plugin_spec(plugin_name, osp.join(base_path, path))
        specs = [spec]
    except KeyError:
        specs = []
        for path in package_spec['paths']:
            path = normalize_crossplatform_path(path)
            module_name = osp.splitext(osp.basename(path))[0]

            spec = get_plugin_spec(f'{plugin_name}.{module_name}',
                                   osp.join(base_path, path))
            specs.append(spec)

    modules = [ module_from_spec(spec) for spec in specs ]

    return modules


def add_namespace_module(install_spec: JSON, modules: List[Module]):
    """If a plugin specifies multiple paths, adds a parent dummy
    namespace module."""
    napari_spec = napari_spec_from_install_spec(install_spec)
    package_spec = package_spec_from_napari_spec(napari_spec)

    plugin_name = package_spec['plugin_name']

    if package_spec.get('paths'):
        modules.append(create_namespace_module(plugin_name))


class entry_points(LazyAttrs):
    before_load_hooks = [update_plugin]
    after_load_hooks = [add_namespace_module,
                        lambda install_spec, modules:
                        make_modules_importable(modules)]

    load_function = find_modules

    activate_function = execute_module

    plugins_spec = lazy(lambda: load_plugins_spec())
    install_specs = lazy(lambda: install_specs_from_plugins_spec(entry_points.
                                                                 plugins_spec))
    modules = []

    cleanup_hooks = [lambda cls: save_plugins_spec(cls.plugins_spec)]

    activated = False


    @classmethod
    def _setup_install_spec(cls, install_spec: JSON) -> List[Module]:
        for before_load_hook in cls.before_load_hooks:
            before_load_hook(install_spec)

        new_modules = cls.load_function(install_spec)

        for after_load_hook in cls.after_load_hooks:
            after_load_hook(install_spec, new_modules)

        cls.modules.extend(new_modules)
        return new_modules

    @classmethod
    def setup(cls):
        for install_spec in cls.install_specs:
            cls._setup_install_spec(install_spec)

    @classmethod
    def activate(cls):
        cls.activated = True
        for module in cls.modules:
            cls.activate_function(module)

    @classmethod
    def add_install_spec(cls, install_spec: JSON):
        new_modules = cls._setup_install_spec(install_spec)
        cls.install_specs.append(install_spec)

        if cls.activated:
            for module in new_modules:
                cls.activate_function(module)

    @classmethod
    def cleanup(cls):
        for cleanup_hook in cls.cleanup_hooks:
            cleanup_hook(cls)
