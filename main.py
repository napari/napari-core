import sys

import vispy
from PyQt5.QtWidgets import QApplication, QAction
import numpy as np

from napari.NapariApplication import NapariApplication
from napari.gui.image_widget import ImageWidget
from vispy import app, gloo, visuals, scene

from napari.gui.image_window import ImageWindow
from napari.utils.napari_utils import load_bluemarble_image

app.use_app('pyqt5')

if __name__ == '__main__':



    # starting
    application = NapariApplication(sys.argv)


    # opening a 2D RGB image:

    bma = load_bluemarble_image(large=True)
    imgdis0 = ImageWindow(bma, 'BlueMarble', window_width=512, window_height=512, is_rgb=True)
    imgdis0.update_image()


    # opening a 2D single channel image:

    h = 5120
    w = 5120
    Y, X = np.ogrid[-2.5:2.5:h * 1j, -2.5:2.5:w * 1j]
    image = np.empty((h, w), dtype=np.float32)
    image[:] = np.random.rand(h, w)
    image[-30:] = np.linspace(0, 1, w)

    imgdis1 = ImageWindow(image, '2D1C', window_width=512, window_height=512)
    imgdis1.set_cmap("viridis")
    #imgdis1.update_image()

    # opening a 3D single channel image:

    h = 512
    w = 512
    d = 512
    Z, Y, X = np.ogrid[-2.5:2.5:h * 1j, -2.5:2.5:w * 1j, -2.5:2.5:d * 1j]
    image = np.empty((h, w, d), dtype=np.float32)
    image[:] = np.exp(- X ** 2 - Y ** 2 - Z ** 2 )  # * (1. + .5*(np.random.rand(h, w)-.5))
    #image[-30:] = np.linspace(0, 1, w)


    imgdis2 = ImageWindow(image, '3D1C', window_width=512, window_height=512)
    imgdis2.set_cmap("blues")
    #imgdis2.show()
    #imgdis2.raise_to_top()

    # opening a 4D single channel image:

    h = 32
    w = 32
    d = 64
    b = 64
    C, Z, Y, X = np.ogrid[-2.5:2.5:h * 1j, -2.5:2.5:w * 1j, -2.5:2.5:d * 1j, -2.5:2.5:b * 1j]
    image = np.empty((h, w, d, b), dtype=np.float32)
    image[:] = np.exp(- X ** 2 - Y ** 2 - Z ** 2 - C ** 2)  # * (1. + .5*(np.random.rand(h, w)-.5))
    # image[-30:] = np.linspace(0, 1, w)


    imgdis3 = ImageWindow(image, '4D1C', window_width=512, window_height=512)
    imgdis3.set_cmap("blues")
    #imgdis3.show()
    #imgdis3.raise_to_top()

    #print(vispy.color.get_colormaps())


    sys.exit(application.exec_())