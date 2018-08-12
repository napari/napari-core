from pathlib import Path

import yaml
import json
from jsonschema import validate

from .._internal.typing import PathLike, JSON


def load_schema(schema_path: PathLike) -> JSON:
    """Loads a schema from a path."""
    schema_path = Path(schema_path).expanduser()
    if not schema_path.is_absolute():
        schema_path = Path(__file__).parent.joinpath(schema_path)

    with schema_path.open('rb') as schema_file:
        return json.loads(schema_file.read())


def find_specification(abs_directory: PathLike, schema: JSON) -> JSON:
    """Finds a specification given its schema."""
    abs_directory = Path(abs_directory).expanduser()

    if not abs_directory.is_absolute():
        raise RuntimeError(f'{abs_directory} is not an absolute path')
    if not abs_directory.is_dir():
        raise RuntimeError(f'{abs_directory} is not a directory')

    file_match = set(schema['fileMatch'])

    for match in file_match:
        path = abs_directory.joinpath(match)
        if path.exists():
            with path.open('rb') as specification_file:
                specification = yaml.load(specification_file.read())
                break
    else:
        raise RuntimeError('No file found matching '
                           + f'{abs_directory.joinpath(str(file_match))}')

    validate(specification, schema)
    return specification
