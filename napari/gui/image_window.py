import platform

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, qApp, QMenuBar

from napari.gui.image_widget import ImageWidget


class ImageWindow(QMainWindow):

    def __init__(self, image, name=None, window_width=800, window_height=800, is_rgb=False, parent=None):

        super(ImageWindow, self).__init__(parent)

        self.widget = ImageWidget(image, name, window_width, window_height, is_rgb)

        self.setCentralWidget(self.widget)

        self.statusBar().showMessage('Ready')

        self.add_menu()
        #self.add_toolbar()
        self.show()

        self.installEventFilter(self)

    def add_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

    def add_menu(self):
        menubar = self.menuBar() # parentless menu bar for Mac OS
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        viewMenu = menubar.addMenu('&Process')
        searchMenu = menubar.addMenu('&Analyse')
        toolsMenu = menubar.addMenu('&Plugins')
        helpMenu = menubar.addMenu('&About')


    def eventFilter(self, object, event):
        #print(event)
        #print(event.type())
        if event.type() == QEvent.ShortcutOverride:
            print(event)
            print(event.key())
            if (event.key() == Qt.Key_F or event.key() == Qt.Key_Enter) and not self.isFullScreen():
                print("showFullScreen!")
                self.showFullScreen()
            elif (event.key() == Qt.Key_F or event.key() == Qt.Key_Escape) and self.isFullScreen():
                print("showNormal!")
                self.showNormal()

        return QWidget.eventFilter(self, object, event)


    def update_image(self):
        self.widget.update_image()

    def set_cmap(self, cmap):
        self.widget.set_cmap(cmap)