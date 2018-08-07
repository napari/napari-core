"""Manages plugins."""
import os.path as osp

from ._config import load_plugins_spec, load_napari_spec, get_abs_plugin_path
from ._git import update_plugin_from_remote
from ._load import NapariPluginFinder

from ..._internal.typing import JSON


def napari_spec_from_install_spec(install_spec: JSON) -> JSON:
    """Loads a napari.yml specification given its install specification."""
    return load_napari_spec(get_abs_plugin_path(install_spec))


def update_plugin(install_spec: JSON):
    """Updates a plugin given its specification."""
    if install_spec.get('development'):
        return

    if install_spec.get('git_source'):
        return update_plugin_from_remote(install_spec)


def load_plugin(install_spec: JSON):
    update_plugin(install_spec)
    napari_spec = napari_spec_from_install_spec(install_spec)
    plugin_spec = napari_spec['plugin_info']

    plugin_name = plugin_spec['plugin_name']

    plugin_dir = get_abs_plugin_path(install_spec)

    try:
        NapariPluginFinder.add_path(plugin_name,
                                    osp.join(plugin_dir, plugin_spec['path']))
    except KeyError:
        NapariPluginFinder.add_paths(plugin_name,
                                     osp.join(plugin_dir,
                                              plugin_spec['paths']))


def on_startup():
    plugins_spec = load_plugins_spec()

    for install_spec in plugins_spec['plugins']:
        load_plugin(install_spec)

    NapariPluginFinder.__install__()


def on_teardown():
    NapariPluginFinder.__uninstall__()
