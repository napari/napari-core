from PyQt5.QtWidgets import QApplication, QAction


class NapariApplication(QApplication):


    def __init__(self, List):
        super(QApplication, self).__init__(List)

