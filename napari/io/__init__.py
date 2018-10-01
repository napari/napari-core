"""
Input/output registration and control hub.
"""
from ._register import input_registry, input, output_registry, output
from ._open import read, write


__all__ = ['input',
           'input_registry',
           'output',
           'output_registry',
           'read',
           'write']
