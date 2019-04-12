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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
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

    def deleteNote(self):
        confirmation = self.askUserConfirmation()
        if confirmation:
            NoteManager.deleteNote(self)
            self.destroy()

    def askUserConfirmation(self):
        msgBox = QMessageBox(self)
        msgBox.setText('Delete this note?')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            return True
        else:
            return False

class NoteMenu(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # create a horizontal layout for the top menu
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 5, 2)
        # add a new note button
        self.new = self.buttonFactory('resources/new.svg', None, self.createNewNote)
        self.layout.addWidget(self.new)
        # add empty space
        self.layout.addStretch(1)
        # add a delete note button
        self.delete = self.buttonFactory('resources/delete.svg', None, self.deleteNote)
        self.layout.addWidget(self.delete)

    def buttonFactory(self, icon, text, handler):
        button = QPushButton(QIcon(icon), text, self)
        button.clicked.connect(handler)
        return button

    def createNewNote(self):
        NoteManager.addNewNote()

    def deleteNote(self):
        self.parentWidget().deleteNote()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftMouseButtonPressed = True
            self.startPosition = self.mapToGlobal(event.pos())

    def mouseMoveEvent(self, event):
        if self.isLeftMouseButtonPressed:
            self.endPosition = self.mapToGlobal(event.pos())
            self.delta = self.endPosition - self.startPosition
            self.newPosition = self.mapToGlobal(self.delta)
            self.parent().setGeometry(self.newPosition.x(), self.newPosition.y(), self.parentWidget().width(), self.parentWidget().height())
            self.startPosition = self.endPosition

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton and self.isLeftMouseButtonPressed:
            self.isLeftMouseButtonPressed = False

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

    @staticmethod
    def deleteNote(note):
        if note in NoteManager.notes:
            NoteManager.notes.remove(note)



