"""
Manages plugins.
"""
import os.path as osp
from warnings import warn

from ._config import (load_plugins_spec, save_plugins_spec,
                      load_napari_spec, install_specs_from_plugins_spec,
                      normalize_crossplatform_path,
                      get_abs_plugin_path, napari_spec_from_install_spec,
                      package_spec_from_napari_spec, entry_points as cep)
from ._git import get_repo, update_plugin_from_remote
from ._load import (get_plugin_spec, module_from_spec, execute_module,
                    create_namespace_module, make_modules_importable,
                    make_namespace_spec, module_name_from_filepath)

from napari.core.lazy import lazy, LazyAttrs
from napari.core.typing import JSON, List, Module, ModuleSpec


try:
    from pip import main as pip_main
except ImportError:  # pip.__version__ >= 10.0.0
    from pip._internal import main as pip_main

PIP_INSTALL = ['install', '-qqq']
IPY_WARN = False


def update_plugin(install_spec: JSON):
    """Updates a plugin with git given its specification."""
    try:
        if install_spec.get('development'):
            return

        repo = get_repo(install_spec)
        remote = install_spec['git_source']
        version = install_spec.get('version')

        update_plugin_from_remote(repo, remote, version)
    except KeyError:
        pass


def install_plugin_pip_reqs(install_spec: JSON):
    """Installs a plugin's pip requirements."""
    try:
        napari_spec = napari_spec_from_install_spec(install_spec)
        pip_requirements = napari_spec['pip_requirements']
    except KeyError:
        pass
    else:
        try:
            __IPYTHON__
        except NameError:
            pass
        else:
            global IPY_WARN
            if not IPY_WARN:
                warn('running from IPython - cannot pip install')
                IPY_WARN = True
            return

        if isinstance(pip_requirements, str):
            # requirements.txt-like file
            path = osp.join(get_abs_plugin_path(install_spec),
                            pip_requirements)
            pip_main(PIP_INSTALL.extend(['-r', path]))
        else:
            pip_main(PIP_INSTALL.extend(pip_requirements))


def find_specs(install_spec: JSON) -> List[ModuleSpec]:
    """Loads module specs given a napari specification."""
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
        specs = [make_namespace_spec(plugin_name)]
        for path in package_spec['paths']:
            path = normalize_crossplatform_path(path)
            module_name = module_name_from_filepath(path)
            module_name = plugin_name + '.' + module_name

            spec = get_plugin_spec(module_name, osp.join(base_path, path))
            specs.append(spec)

    return specs


def find_modules(install_spec: JSON) -> List[Module]:
    """Loads modules given a napari specification."""
    modules = [ module_from_spec(spec) for spec in find_specs(install_spec) ]

    return modules


class entry_points(LazyAttrs):
    before_load_hooks = [update_plugin,
                         install_plugin_pip_reqs]
    after_load_hooks = [lambda install_spec, modules:
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
