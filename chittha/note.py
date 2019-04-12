from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
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
        # create a topmost vertical layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # add widgets to the layout
        self.menu = NoteMenu(self)
        self.layout.addWidget(self.menu)
        self.editor = NoteEditor(self)
        self.layout.addWidget(self.editor)
        self.statusBar = NoteStatus(self)
        self.layout.addWidget(self.statusBar)
        # add the layout to the note widget
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
        # create a horizontal layout for the top menu
        self.layout = QHBoxLayout(self)
        self.new = self.buttonFactory('resources/new.svg', 'new', self.createNewNote)
        self.layout.addWidget(self.new)

    def buttonFactory(self, icon, text, handler):
        button = QPushButton(QIcon(icon), text, self)
        button.clicked.connect(handler)
        return button

    def createNewNote(self):
        NoteManager.addNewNote()

class NoteEditor(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)

class NoteStatus(QStatusBar):

    def __init__(self, parent):
        super().__init__(parent)

class NoteManager:

    notes = []

    @staticmethod
    def addNewNote():
        note = Note()
        note.showNote()
        note.activateWindow()
        NoteManager.notes.append(note)

