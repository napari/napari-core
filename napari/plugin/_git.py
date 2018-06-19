"""Retrieves and manages plugins using git.
"""
import git

from .config import plugins_path
from .._internal.errors import NapariError


git_cmd = git.Git(plugins_path)


def valid_remote(remote: str) -> bool:
    """Determines if the link is a valid git remote."""
    return remote.endswith('.git')


def remote_name(remote: str) -> str:
    """Determines a remote repository's name."""
    if valid_remote(remote):
        remote = remote[:-4]
    remote = remote.split(':')[-1]
    return remote.split('/')[-1]


def clone_repo(remote: str) -> str:
    """Clones a repository to the 'config/plugins' directory.

    Parameters
    ----------
    remote : str
        The http or ssh link to the remote repository.

    Returns
    -------
    repo_name : str
        The name of the cloned repository.

    Raises
    ------
    NapariError
        When the link is not a valid git repository.
    """
    if not valid_remote(remote):
        raise NapariError('Not a valid git repository: %s' % remote,
                          display='inline')
    git_cmd.clone(remote)
    return remote_name(remote)
