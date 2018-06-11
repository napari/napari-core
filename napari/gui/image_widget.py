# pythonprogramminglanguage.com
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)

from napari.gui.image_canvas import ImageCanvas


class ImageWidget(QWidget):

    def __init__(self, image, name=None, window_width=800, window_height=800, parent=None):
        super(ImageWidget, self).__init__(parent)

        self.image = image
        self.name = name



        self.resize(window_width, window_height)

        self.image_canvas = ImageCanvas(self, window_width, window_height)

        self.image_canvas.set_image(image)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 10);
        grid.setColumnStretch(0,4)
        grid.setRowStretch(0, 4)
        grid.addWidget(self.image_canvas.native, 0, 0)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickInterval(10)
        slider.setSingleStep(1)

        def value_changed(self):
            self.image_canvas.setBrightness(slider.value()*0.01)


        slider.valueChanged.connect(value_changed)

        grid.addWidget(slider, 1, 0)
        #grid.addWidget(self.createExampleGroup("0,1"), 0, 1)
        #grid.addWidget(self.createExampleGroup("1,1"), 1, 1)


        self.setLayout(grid)

        self.update_title()



    def update_title(self):
        name = self.name

        if self.name is None:
            name = ''

        title = "Image %s %s %s" % (name, str(self.image.shape), self.image_canvas.get_interpolation_name())
        self.setWindowTitle(title)


    def set_cmap(self, cmap):
      if self.image_canvas is not None:
          self.image_canvas.set_cmap(cmap)

    def on_key_press(self, event):
        #print(event.key)
        if (event.key == 'F' or event.key == 'Enter') and not self.isFullScreen():
            #print("showFullScreen!")
            self.showFullScreen()
        elif (event.key == 'F' or event.key == 'Escape') and self.isFullScreen():
            #print("showNormal!)
            self.showNormal()
        elif event.key == 'I':
            self.image_canvas.increment_interpolation_index()
            self.update_title()

    def raise_to_top(self):
        super().raise_()

