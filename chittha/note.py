from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint

class Note(QWidget):

    MIN_WIDTH = 140
    MIN_HEIGHT = 120
    INITIAL_WIDTH = 280
    INITIAL_HEIGHT = 240

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMinimumHeight(self.MIN_HEIGHT)
        self.resize(self.INITIAL_WIDTH, self.INITIAL_HEIGHT)
        self.setWindowFlags(Qt.Tool)
        self.currentPosition = None

    def hideNote(self):
        self.currentPosition = self.pos()
        self.hide()

    def showNote(self):
        self.hide()
        if self.currentPosition:
            self.move(self.currentPosition)
        self.show()
        self.activateWindow()
