"""Collection of enumeration types.
"""
from enum import Enum, auto


class AutoName(Enum):
    """Enum whose auto-generated values are the names of the options.

    References
    ----------
    ..[1] https://docs.python.org/3/library/enum.html#using-automatic-values
    """
    def _generate_next_value_(name, start, count, last_values):
        return name


class Display(AutoName):
    LOG = auto()       # write to a log file
    EMBEDDED = auto()  # display directly in the interface
    POPUP = auto()     # create a popup dialog
