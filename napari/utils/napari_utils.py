import numpy

__bluemarble_url = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x5400x2700.jpg'
__bluemarble_large_url = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57730/land_ocean_ice_8192.png'
__bluemarble_verylarge_url = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x21600x10800.jpg'

from PIL import Image
import requests
from io import BytesIO


def load_bluemarble_image(large = False):
    if large:
        return load_image_array_from_url(__bluemarble_large_url)
    else:
        return load_image_array_from_url(__bluemarble_url)


def load_image_array_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    array = numpy.array(img)
    print(array.shape)
    return array