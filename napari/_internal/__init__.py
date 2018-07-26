import sys

from skimage._shared import testing


sys.modules[f'{__name__}.testing'] = testing


del sys
