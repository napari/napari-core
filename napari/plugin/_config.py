"""Handles plugin configuration."""
import os
import os.path as osp
import re

import yaml
import json
import jsonschema

from typing import NewType, Union

from .._internal import paths
from .._internal.errors import NapariError


JSON = NewType('JSON', Union[dict, list])

plugins_path = paths.create_config_path('plugins')
plugins_index_pattern = 'index.(?P<ext>json|ya?ml)$'

schema_path = osp.join(osp.dirname(__file__), 'index_schema.json')

with open(schema_path, 'r') as schema_file:
    index_schema = json.loads(schema_file.read())


def fetch_index_contents(index_dir: str) -> JSON:
    """Fetches the contents of the matching index file.

    Parameters
    ----------
    index_dir : str
        Parent directory of the index file.

    Returns
    -------
    index_contents : JSON
        Contents of the index file in JSON.

    Raises
    ------
    NapariError
        When there is not exactly one index file in the directory.
    """
    index_paths = []

    for fname in os.listdir(index_dir):
        match = re.match(plugins_index_pattern, fname, re.IGNORECASE)
        if match:
            print(fname)
            fpath = osp.join(index_dir, fname)

            index_paths.append(fpath)
            ext = match.groupdict()['ext']


    if len(index_paths) == 0:
        raise NapariError('No index file found in %s' % index_dir,
                          display='popup')

    if len(index_paths) > 1:
        raise NapariError('Multiple index files found in %s: %s'
                          % (index_dir, index_paths),
                          displa='popup')

    index_path = index_paths[0]

    with open(index_path, 'r') as index_file:
        ext = ext.lower()
        if ext == 'json':
            index_contents = json.loads(index_file)
        elif ext in ('yml', 'yaml'):
            index_contents = yaml.load(index_file)

    return index_contents


def validate_index(index: JSON) -> bool:
    """Determines whether the given index contents are valid."""
    try:
        jsonschema.validate(index, index_schema)
        return True
    except ValidationError:
        return False
