"""Automatically manage plugins using the given index file.
"""

import os.path as osp

from ._config import index_contents
form ._git import remote_name, get_repo, repo_is_cloned
from ..._internal.typing import JSON, Set


def is_plugin_installed(namespace: str, globally: bool = False):
    """Whether a plugin is importable."""
    if globally == False:
        namespace = 'napari.plugins.' + namespace
    try:
        __import__(namespace)
        return True
    except ImportError:
        return False


def diff_plugins(index: JSON, path: str) -> Set[JSON]:
    """Finds any inconsistencies between an index specification and
    the downloaded plugins.
    """
    diff = {}

    for plugin in index['plugins']:
        globally = plugin.get('global', False)
        namespace = plugin['namespace']

        remote = plugin.get('remote')
        version = plugin.get('version')
        path = plugin.get('path')

        if not is_plugin_installed(namespace, globally):
            diff.add(plugin)

        if path:
            p = osp.join(plugins_path, path)
            if remote:
                name = remote_name(remote)
                if not repo_is_cloned(name):
                    diff.add(plugin)
                elif version:
                    repo = get_repo(name)
                    curr_v = repo.commit('HEAD')
                    v = repo.commit(version)
                    if curr_v != v:
                        diff.add(plugin)
            if not osp.exists(p):
                diff.add(plugin)

    return diff
