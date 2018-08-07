"""Handles plugin configuration."""
import os.path as osp

from napari.specifications import load_schema, find_specification

from ..._internal import paths
from ..._internal.typing import JSON, PathLike


plugins_path = paths.create_config_path('plugins')
plugins_spec_schema = load_schema('plugins_yml_schema.json')
napari_spec_schema = load_schema('napari_yml_schema.json')


def load_plugins_spec(abs_directory: PathLike = paths.config_path) -> JSON:
    """Loads a plugins.yml specification."""
    return find_specification(abs_directory, plugins_spec_schema)


def load_napari_spec(abs_directory: PathLike) -> JSON:
    """Loads a napari.yml specification."""
    return find_specification(abs_directory, napari_spec_schema)


def get_abs_plugin_path(install_spec: JSON) -> str:
    """Gets the path of the specified plugin."""
    try:
        folder = install_spec['folder']
    except KeyError:
        from ._git import repo_name_from_remote  # prevents import loop
        folder = repo_name_from_remote(install_spec['git_source'])

    return osp.join(plugins_path, folder)
