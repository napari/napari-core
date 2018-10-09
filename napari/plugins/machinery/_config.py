"""
Handles plugin configuration.
"""
import os.path as osp

from napari.core.specs import load_schema, load_spec, save_spec

from napari.core import paths
from napari.core.lazy import lazy, LazyAttrsClass
from napari.core.typing import JSON, PathLike, List, Optional


def load_plugins_spec(abs_dir: Optional[PathLike] = paths.config_path) -> JSON:
    """Loads a plugins.yml specification."""
    spec = load_spec(abs_dir, entry_points.plugins_spec_schema)
    if spec is None:
        spec = dict(plugins=[])

    return spec


def save_plugins_spec(spec: JSON,
                      abs_dir: Optional[PathLike] = paths.config_path
                      ) -> PathLike:
    """Saves the plugins.yml specification."""
    return save_spec(spec, abs_dir, entry_points.plugins_spec_schema)


def load_napari_spec(abs_dir: PathLike) -> JSON:
    """Loads a napari.yml specification."""
    return load_spec(abs_dir, entry_points.napari_spec_schema)


def normalize_crossplatform_path(path: str) -> PathLike:
    """Normalizes cross-platform paths by replacing / with the proper
    path separator."""
    return path.replace('/', osp.sep)


def get_abs_plugin_path(install_spec: JSON) -> str:
    """Gets the path of the specified plugin."""
    try:
        folder = install_spec['folder']
        folder = osp.expanduser(folder)
    except KeyError:
        from ._git import repo_name_from_remote  # prevents import loop
        folder = repo_name_from_remote(install_spec['git_source'])

    if not osp.isabs(folder):
        return osp.join(entry_points.plugins_path, folder)
    return folder


def install_specs_from_plugins_spec(plugins_spec: JSON) -> List[JSON]:
    """Finds the install specifications from the plugins specification."""
    return plugins_spec['plugins']


def napari_spec_from_install_spec(install_spec: JSON) -> JSON:
    """Loads a napari specification given its install specification."""
    return load_napari_spec(get_abs_plugin_path(install_spec))


def package_spec_from_napari_spec(napari_spec: JSON) -> JSON:
    """Finds the package specification from the napari specification."""
    return napari_spec['plugin_info']


class entry_points(LazyAttrsClass):
    plugins_path = lazy(lambda: paths.create_config_path('plugins'))
    plugins_spec_schema = lazy(lambda: load_schema('plugins_yml_schema.json'))
    napari_spec_schema = lazy(lambda: load_schema('napari_yml_schema.json'))
