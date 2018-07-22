"""Retrieves and manages plugins using git.
"""
import os.path as osp
import re

import git

from ._config import plugins_path
from ..._internal.typing import Progress, Optional, List
from ..._internal.errors import NapariError


remote_pattern = (r'^(?:[^:\/?#]+:)?(?:\/\/[^\/?#]*)?[^?#]*?'
                  r'(?P<name>[^\/:]+)\.git$')


def repo_name(remote: str) -> str:
    """Determines a remote repository's name."""
    match = re.match(remote_pattern, remote)
    if not match:
        raise NapariError('Not a valid git repository: %s' % remote,
                          display='inline')
    return match.groupdict()['name']


def get_repo_path(repo_name: str) -> str:
    """Gets the path of the specified plugin repo."""
    return osp.join(plugins_path, repo_name)


def clone_remote(remote: str, progress: Optional[Progress] = None) -> git.Repo:
    """Clones a repository to the 'config/plugins' directory.

    Parameters
    ----------
    remote : str
        URI for the remote repository.
    progress : git.RemoteProgress or ProgressCallback, optional
        Update callback for the progress on a remote git operation.
        ``callback(op_code, cur_count, max_count=None, message='')``

    Returns
    -------
    repo_name : git.Repo
        Cloned repository.

    Raises
    ------
    NapariError
        When the URI is not a valid git repository.
    """
    name = repo_name(remote)
    path = get_repo_path(name)

    return git.Repo.clone_from(remote, path, progress=progress)


def update_remote_branch(remote: git.Remote, loc: str, rem: str,
                         progress: Progress, **kwargs) -> List[git.PushInfo]:
    """Pushes to the specified branch of the remote repository."""
    return remote.push(f'{local}:{remote}', progress=progress, **kwargs)


def delete_remote_branch(remote: git.Remote, branch: str, progress: Progress,
                         **kwargs) -> List[git.PushInfo]:
    """Deletes the specified branch of the remote repostiory."""
    return update_remote_branch('', branch, progress, **kwargs)


def get_repo(repo_name: str) -> git.Repo:
    """Gets the specified repo."""
    return git.Repo(get_repo_path(repo_name))


def repo_is_cloned(repo_name: str) -> bool:
    """Checks if a repo has been downloaded already."""
    return osp.exists(osp.join(plugins_path, repo_name))
