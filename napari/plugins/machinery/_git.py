"""Retrieves and manages plugins using git.
"""
import os.path as osp
import re

from git import Repo

from ._config import plugins_path, get_abs_plugin_path
from ..._internal.typing import JSON, Progress, Optional, List
from ..._internal.errors import NapariError


remote_pattern = (r'^(?:[^:\/?#]+:)?(?:\/\/[^\/?#]*)?[^?#]*?'
                  r'(?P<name>[^\/:]+)\.git$')


def repo_name_from_remote(remote: str) -> str:
    """Determines a remote repository's name."""
    match = re.match(remote_pattern, remote)
    if not match:
        raise NapariError('Not a valid git repository: %s' % remote,
                          display='inline')
    return match.groupdict()['name']


def get_repo(install_spec: JSON) -> Repo:
    """Gets the specified repo."""
    return Repo.init(get_abs_plugin_path(install_spec))


def init_repo_source(repo: Repo, install_spec: JSON) -> Repo:
    """Initializes the specified repo's source remote."""
    remote = install_spec['git_source']

    try:
        source = repo.remote('source')
        if remote not in source.urls:
            source.set_url(remote)
    except ValueError as e:
        if str(e) != "Remote named 'source' didn't exist":
            raise e
        source = repo.create_remote('source', remote)

    return source


def update_plugin_from_remote(install_spec: JSON,
                              progress: Optional[Progress] = None):
    """Updates a plugin from a remote Git repository."""
    repo = get_repo(install_spec)

    source = init_repo_source(repo, install_spec)

    # TODO: handle 'redirect' responses here
    source.fetch(progress=progress)

    version = install_spec.get('version') or 'FETCH_HEAD'

    repo.git.checkout(version, B='source')
