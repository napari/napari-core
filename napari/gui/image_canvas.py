
from OpenGL import GL
from OpenGL.raw.GL.VERSION.GL_1_0 import glMatrixMode, glLoadIdentity
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_PROJECTION
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
from OpenGL.GL.ARB.texture_rg import GL_R32F

import numpy as np
import ctypes
import time

from vispy import scene
from vispy.app import Canvas
from vispy.io import read_png
from vispy.scene import SceneCanvas
from vispy.util import load_data_file

from napari.gui.panzoom import PanZoomCamera


class ImageCanvas(SceneCanvas):

    def __init__(self, parent_widget, window_width, window_height):
        super(ImageCanvas, self).__init__(keys=None, vsync=True)

        self.size = window_width, window_height

        self.unfreeze()

        self.image_visual = None
        self.brightness = 1
        self.parent_widget = parent_widget
        self.title = "image"
        self.image = None
        # Set up a viewbox to display the image with interactive pan/zoom
        self.view = self.central_widget.add_view()
        self.interpolation = 'nearest'

        self.image_visual = scene.visuals.Image(None, interpolation=self.interpolation,
                                                parent=self.view.scene, method='subdivide')

        self.freeze()




    def set_image(self, name, image, dimx=0, dimy=1):

        self.title = name
        self.image = image
        self.image_visual.set_data(image)
        self.view.camera.set_range()

        # Set 2D camera (the camera will scale to the contents in the scene)
        self.view.camera = PanZoomCamera(aspect=1)
        # flip y-axis to have correct aligment
        self.view.camera.flip = (0, 1, 0)
        self.view.camera.set_range()
        # view.camera.zoom(0.1, (250, 200))



    def on_key_press(self, event):
        #print("Sending to QT parent: %s " % event.key)
        self.parent_widget.on_key_press(event)


    def setBrightness(self, brightness):
        print("brightess = %f" % brightness)
        self.brightness = brightness
        self.update()

    def set_cmap(self, cmap):
        self.image_visual.cmap = cmap
        self.update()


