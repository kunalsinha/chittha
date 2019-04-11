from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QStatusBar
from PyQt5.QtCore import Qt, QPoint

import logging

logger = logging.getLogger(__name__)

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
        # make the note widgets skip taskbar
        self.setWindowFlags(Qt.Tool)
        self.currentPosition = None
        # add a topmost vertical layout to the note
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(NoteMenu(self))
        self.layout.addWidget(NoteEditor(self))
        self.layout.addWidget(NoteStatus(self))
        self.setLayout(self.layout)

    def hideNote(self):
        if not self.isHidden:
            self.currentPosition = self.pos()
        self.hide()
        self.isHidden = True
        logger.error('Hiding at: ' + str(self.currentPosition))

    def showNote(self):
        self.hide()
        if self.currentPosition:
            self.move(self.currentPosition)
            logger.error('Moving to: ' + str(self.currentPosition))
        self.show()
        self.activateWindow()
        self.isHidden = False

class NoteMenu(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

class NoteEditor(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)

class NoteStatus(QStatusBar):

    def __init__(self, parent):
        super().__init__(parent)

