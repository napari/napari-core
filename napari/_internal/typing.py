"""Commonly used types.
"""
from typing import *
from typing import __all__

__all__ += ['JSON']


JSON = NewType('JSON', Union[List, Dict])
