"""
Collection of Napari-generated exceptions.
"""
from napari.core.enums import Display
from typing import Union


class NapariError(Exception):
    """Base class for Napari-generated exceptions.

    Attributes
    ----------
    message : str
        Message to display.
    display : {'log', 'embedded', 'popup'}
        Medium for displaying the message.
    """
    __slots__ = ('message', 'display')

    def __init__(self, message: str, display: Union[str, Display]):
        self.message = message
        self.display = display


class InputError(NapariError):
    """Signals an error in the input with argument checkings."""
    __slots__ = ()

    def __init__(self, message, display='embedded'):
        super().__init__(message, display)


class ExternalError(NapariError):
    """Wraps an exception raised by another package.

    Attributes
    ----------
    message : str
        Message to display.
    exception : Exception
        Parent exception.
    display : {'log', 'embedded', 'popup'}
        Medium for displaying the message.
    """
    __slots__ = ('exception',)

    def __init__(self, message, exception, display='log'):
        super().__init__(message, display)
        self.exception = exception
