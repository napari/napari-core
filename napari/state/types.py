"""
Type definitions used by the state module.
"""
from napari.core.typing import Type, Callable


ExtractFunc = Callable[['State'], object]
PopulateFunc = Callable[[object, 'State'], 'State']


class IncompatibilityError(TypeError):
    """Signals that there is no conversion from one type to another.
    """
    def __init__(self, from_type: Type, to_type: Type):
        message = f'No conversion found from {from_type} to {to_type}'
        super().__init__(message)
