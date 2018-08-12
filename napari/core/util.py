import shlex
import subprocess

from .typing import List


def call(cmd: str) -> List[str]:
    """Makes a call on the command line."""
    return subprocess.check_output(shlex.split(cmd),
                                   universal_newlines=True).split('\n')
