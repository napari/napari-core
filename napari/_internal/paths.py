"""Filepath utilities.
"""
import os as _os
import os.path as osp


_file_path = osp.abspath(__file__)
_dir_path = osp.dirname(_file_path)
package_path = osp.dirname(_dir_path)
base_path = osp.dirname(package_path)
config_path = osp.join(base_path, 'config')


def make_config_path(dirname: str) -> str:
    """Generates a new configuration path."""
    return osp.join(config_path, dirname)


def mkdir(path: str) -> bool:
    """Creates a directory. If it already exists, returns True."""
    try:
        _os.makedirs(path)
        return False
    except FileExistsError:
        return True


def create_config_path(dirname: str) -> str:
    """Creates a new configuration path and its parents if they does not exist.
    """
    path = make_config_path(dirname)
    mkdir(path)
    return path
