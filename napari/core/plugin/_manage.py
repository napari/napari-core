"""Automatically manage plugins using the given index file.
"""
import os
import os.path as osp
import git

from ._config import index_contents, plugins_path, custom_submodule_path
from ._git import repo_name, clone_remote, get_repo, repo_is_cloned
from ..._internal.typing import JSON, Iterable, List, Progress, Optional
from ..._internal.util import call


def is_plugin_installed(namespace: str, globally: bool = False):
    """Whether a plugin is importable."""
    if globally == False:
        namespace = 'napari.plugins.' + namespace
    try:
        __import__(namespace)
        return True
    except ImportError:
        return False


def diff_plugin(plugin: JSON) -> bool:
    """Returns True if a plugin is inconsistent with its specification."""
    globally = plugin.get('global', False)
    namespace = plugin['namespace']

    remote = plugin.get('remote')
    version = plugin.get('version')
    path = plugin.get('path')

    if not is_plugin_installed(namespace, globally):
        return True

    if path:
        p = osp.join(plugins_path, path)
        if remote:
            name = repo_name(remote)
            if not repo_is_cloned(name):
                return True
            elif version:
                repo = get_repo(name)
                curr_v = repo.commit('HEAD')
                v = repo.commit(version)
                if curr_v != v:
                    return True
        if not osp.exists(p):
            return True


def update_plugin(plugin: JSON,
                  progress: Optional[Progress] = None):
    """Updates a plugin according to its given specification."""
    try:
        update_plugin_from_remote(plugin['remote'],
                                  plugin['version'],
                                  plugin.get('remote-name') or 'origin',
                                  progress=progress)
    except KeyError:
        pass


def update_plugin_from_remote(remote: str, version: str, remote_name: str,
                              progress: Optional[Progress] = None):
    """Updates a plugin from a remote Git repository."""
    name = repo_name(remote)

    if repo_is_cloned(name):
        repo = get_repo(name)
    else:
        repo = clone_remote(remote, progress=progress)

    try:
        rem = repo.remote(remote_name)
    except ValueError as e:
        if str(e) != f"Remote named '{remote_name}' didn't exist":
            raise
        rem = git.Remote(repo, remote_name)

    rem.set_url(remote)
    fi = rem.fetch(f'{repo.head.ref.name}', progress=progress)[0]
    repo.head.ref.commit = fi.commit

    if version:
        repo.head.ref.commit = repo.commit(version)

    repo.head.reset(working_tree=True)


def install_plugin(plugin: JSON):
    """Installs a plugin according to its given specification."""
    if plugin.get('install'):
        for cmd in plugin['install']:
            call(cmd)

    if plugin.get('path'):
        path = osp.join(plugins_path, plugin['path'])
        namespace_path = osp.join(custom_submodule_path, plugin['namespace'])
        if osp.exists(namespace_path):
            if os.readlink(namespace_path) != path:
                os.unlink(namespace_path)
            return
        os.symlink(path, namespace_path)
