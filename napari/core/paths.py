"""
Filepath utilities.
"""
import os
import os.path as osp

import re

import yaml
import json

from napari.core.typing import JSON


_file_path = osp.abspath(__file__)
_dir_path = osp.dirname(_file_path)
package_path = osp.dirname(_dir_path)
base_path = osp.dirname(package_path)
config_path = osp.join(base_path, 'config')

config_file_pattern = r'\.(?P<ext>json|ya?ml)$'


def get_config_path(dirname: str) -> str:
    """Gets a configuration path."""
    return osp.join(config_path, dirname)


def mkdir(path: str) -> bool:
    """Creates a directory. If it already exists, returns True."""
    try:
        os.makedirs(path)
        return False
    except FileExistsError:
        return True


def create_config_path(dirname: str) -> str:
    """Creates a new configuration path and its parents if they does not exist.
    """
    path = get_config_path(dirname)
    mkdir(path)
    return path
