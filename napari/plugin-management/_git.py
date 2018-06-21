"""Retrieves and manages plugins using git.
"""
import re
import git

from ._config import plugins_path
from .._internal.errors import NapariError


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


def clone_repo(remote: str) -> str:
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
