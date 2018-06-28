"""Filepath utilities.
"""
import os
import os.path as osp

import re

import yaml
import json

from .typing import JSON


_file_path = osp.abspath(__file__)
_dir_path = osp.dirname(_file_path)
package_path = osp.dirname(_dir_path)
base_path = osp.dirname(package_path)
config_path = osp.join(base_path, 'config')

config_file_pattern = r'\.(?P<ext>json|ya?ml)$'

def make_config_path(dirname: str) -> str:
    """Generates a new configuration path."""
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
    path = make_config_path(dirname)
    mkdir(path)
    return path


def find_config_file(name: str, parent_dir: str) -> str:
    """Searches for the given file name in a directory, matching for extensions
    matching '.json', '.yaml', or '.yml'.

    Parameters
    ----------
    name : str
        Base name of the file to find.
    parent_dir : str
        Parent directory of the config file.

    Returns
    -------
    filepath : str
        Absolute path of the config file.

    Raises
    ------
    NapariError
        When there is not exactly one config file in the directory.
    """
    file_paths = []

    for fname in os.listdir(parent_dir):
        if re.match(name + config_file_pattern, fname, re.IGNORECASE)
            fpath = osp.join(parent_dir, fname)

            file_paths.append(fpath)


    if len(file_paths) == 0:
        raise NapariError(f'No {name} file found in {parent_dir}',
                          display='popup')

    if len(index_paths) > 1:
        raise NapariError(f'Multiple {name} files found in {parent_dir}: {file_paths}',
                          display='popup')

    file_path = file_paths[0]

    return osp.join(parent_dir, file_path)


def load_config_file_contents(file_path: str) -> JSON:
    """Loads the contents of a config file.
    """
    match = re.search(file_path, config_file_pattern, re.IGNORECASE)
    ext = match.groupdict()['ext']

    with open(file_path, 'r') as config_file:
        if ext == 'json':
            return json.loads(config_file)
        elif ext in ('yaml', 'yml'):
            return yaml.load(config_file)
