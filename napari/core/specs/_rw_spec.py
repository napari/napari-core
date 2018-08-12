import os.path as osp

import yaml
import json
from jsonschema import validate as validate_spec

from napari.core.typing import PathLike, JSON


def load_schema(schema_path: PathLike) -> JSON:
    """Loads a schema from a path."""
    schema_path = osp.expanduser(schema_path)
    if not osp.isabs(schema_path):
        schema_path = osp.join(osp.dirname(__file__), schema_path)

    with open(schema_path, 'rb') as schema_file:
        return json.loads(schema_file.read())


def find_spec_path(abs_dir: PathLike, schema: JSON) -> PathLike:
    """Finds a specification's path given its schema."""
    abs_dir = osp.expanduser(abs_dir)

    if not osp.isabs(abs_dir):
        raise RuntimeError(f'{abs_dir} is not an absolute path')
    if not osp.isdir(abs_dir):
        raise RuntimeError(f'{abs_dir} is not a directory')

    file_match = set(schema['fileMatch'])

    for match in file_match:
        path = osp.join(abs_dir, match)
        if osp.exists(path):
            break
    else:
        raise FileNotFoundError('No file found matching '
                                '{osp.join(abs_dir, file_match)}')

    return path


def load_spec(abs_dir: PathLike, schema: JSON) -> JSON:
    """Loads a specification given its schema."""
    with open(find_spec_path(abs_dir, schema), 'rb') as spec_file:
        spec = yaml.load(spec_file.read())

    validate_spec(spec, schema)
    return spec


def save_spec(spec: JSON, abs_dir: PathLike, schema: JSON) -> PathLike:
    """Saves a specification given its schema."""
    try:
        spec_path = find_spec_path(abs_dir, schema)
    except FileNotFoundError:
        spec_path = schema['fileMatch'][0]

    with open(spec_path, 'wb') as spec_file:
        yaml.dump(spec, spec_file, allow_unicode=True)

    return spec_path
