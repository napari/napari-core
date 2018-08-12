"""Type definitions.
"""
import typing as typ
from typing import NewType, Union


Maybe = typ.Optional
JSON = NewType('JSON', Union[dict, list])
