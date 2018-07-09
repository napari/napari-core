"""Retrieves and manages plugins using git.
"""
import os.path as osp
import re

import git

from ._config import plugins_path
from ..._internal.errors import NapariError


remote_pattern = (r'^(?:[^:\/?#]+:)?(?:\/\/[^\/?#]*)?[^?#]*?'
                  r'(?P<name>[^\/:]+)\.git$')
git_cmd = git.Git(plugins_path)


def remote_name(remote: str) -> str:
    """Determines a remote repository's name."""
    match = re.match(remote_pattern, remote)
    if not match:
        raise NapariError('Not a valid git repository: %s' % remote,
                          display='inline')
    return match.groupdict()['name']


def clone_remote(remote: str) -> str:
    """Clones a repository to the 'config/plugins' directory.

    Parameters
    ----------
    remote : str
        URI for the remote repository.

    Returns
    -------
    repo_name : str
        Name of the cloned repository.

    Raises
    ------
    NapariError
        When the URI is not a valid git repository.
    """
    name = remote_name(remote)
    git_cmd.clone(remote)

    return name


def get_repo(repo_name: str) -> git.Repo:
    """Gets the specified repo."""
    return git.Repo(osp.join(plugins_path, repo_name))


def repo_is_cloned(repo_name: str) -> bool:
    """Checks if a repo has been downloaded already."""
    return osp.exists(osp.join(plugins_path, repo_name))
