"""
Input/output registration and control hub.
"""
from ._rw_register import (read_file_ext, read_file_ext_registry,
                           write_file_ext, write_file_ext_registry)
from ._open import read, write


__all__ = ['read',
           'read_file_ext',
           'read_file_ext_registry',
           'write',
           'write_file_ext',
           'write_file_ext_registry']
