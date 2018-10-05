"""
Input/output registration and control hub.
"""
from ._rw_register import (reads_file_ext, reads_file_ext_registry,
                           writes_file_ext, writes_file_ext_registry)
from ._open import read, write


__all__ = ['read',
           'reads_file_ext',
           'reads_file_ext_registry',
           'write',
           'writes_file_ext',
           'writes_file_ext_registry']
