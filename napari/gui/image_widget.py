# pythonprogramminglanguage.com
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)

from napari.gui.image_canvas import ImageCanvas


class ImageWidget(QWidget):

    def __init__(self, image, parent=None):
        super(ImageWidget, self).__init__(parent)

        image_widget = ImageCanvas()

        image_widget.set_image("image",image)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 10);
        grid.setColumnStretch(0,4)
        grid.setRowStretch(0, 4)
        grid.addWidget(image_widget.native, 0, 0)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickInterval(10)
        slider.setSingleStep(1)

        def value_changed(self):
            image_widget.setBrightness(slider.value()*0.01)


        slider.valueChanged.connect(value_changed)

        grid.addWidget(slider, 1, 0)
        #grid.addWidget(self.createExampleGroup("0,1"), 0, 1)
        #grid.addWidget(self.createExampleGroup("1,1"), 1, 1)


        self.setLayout(grid)

        self.setWindowTitle("ImageDisplay")
        self.resize(400, 300)


