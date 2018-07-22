"""Handles plugin configuration."""
import os
import os.path as osp
import re

import jsonschema

from ..._internal import paths
from ..._internal.errors import NapariError
from ..._internal.typing import JSON


def validate_index(index: JSON):
    """Validates index contents against schema.

    Raises
    ------
    NapariError
        When the index contents are invalid.
    """
    try:
        jsonschema.validate(index, index_schema)
    except jsonschema.ValidationError as e:
        raise NapariError(e.message, display='embedded')


plugins_path = paths.create_config_path('plugins')
custom_submodule_path = osp.join(paths.package_path, 'plugins')

schema_path = osp.join(osp.dirname(__file__), 'index_schema.json')

with open(schema_path, 'r') as schema_file:
    index_schema = paths.json.loads(schema_file.read())

index_file = paths.find_config_file('index', plugins_path)
index_contents = paths.load_config_file_contents(index_file)
validate_index(index_contents)
