from PyQt5.Qt import QStandardPaths
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import *
from chittha import utils
import json
import logging

logger = logging.getLogger(__name__)

class Note(QWidget):

    MIN_WIDTH = 140
    MIN_HEIGHT = 120
    INITIAL_WIDTH = 280
    INITIAL_HEIGHT = 240
    flags = Qt.FramelessWindowHint | Qt.Tool

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMinimumHeight(self.MIN_HEIGHT)
        self.resize(self.INITIAL_WIDTH, self.INITIAL_HEIGHT)
        # make the note widgets skip taskbar
        self.setWindowFlags(Note.flags)
        # initialize needed properties
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
        # register shortcuts
        self.registerShortcuts()

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

    def lockNote(self):
        self.editor.setReadOnly(not self.editor.isReadOnly())

    def registerShortcuts(self):
        self.registerShortcut('Ctrl+N', NoteManager.addNewNote)
        self.registerShortcut('Ctrl+Shift+H', NoteManager.hideAllNotes)
        self.registerShortcut('Ctrl+Shift+S', NoteManager.showAllNotes)

    def registerShortcut(self, sequence, handler):
        shortcut = QShortcut(QKeySequence(sequence), self)
        shortcut.activated.connect(handler)


class NoteMenu(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # create a horizontal layout for the top menu
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 5, 2)
        # add a lock note button
        self.lock = self.buttonFactory('resources/lock.svg', None, self.lockNote)
        self.layout.addWidget(self.lock)
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

    def lockNote(self):
        self.parentWidget().lockNote()

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
            self.parentWidget().setGeometry(self.newPosition.x(), self.newPosition.y(), self.parentWidget().width(), self.parentWidget().height())
            self.startPosition = self.endPosition
            self.parentWidget().currentPosition = self.newPosition

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton and self.isLeftMouseButtonPressed:
            self.isLeftMouseButtonPressed = False

class NoteEditor(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

class NoteStatus(QStatusBar):

    def __init__(self, parent):
        super().__init__(parent)

class NoteManager:

    notes = []
    ALWAYS_ON_TOP = False

    @staticmethod
    def addNewNote():
        note = Note()
        note.showNote()
        note.activateWindow()
        note.editor.setFocus()
        NoteManager.notes.append(note)

    @staticmethod
    def deleteNote(note):
        if note in NoteManager.notes:
            NoteManager.notes.remove(note)

    @staticmethod
    def cloneNote(note):
        clone = Note()
        clone.setGeometry(note.geometry())
        clone.setWindowFlags(Note.flags)
        clone.editor.setPlainText(note.editor.toPlainText())
        clone.currentPosition = note.pos()
        NoteManager.notes.remove(note)
        note.destroy()
        clone.showNote()
        clone.activateWindow()
        NoteManager.notes.append(clone)

    @staticmethod
    def toggleAlwaysOnTop(alwaysOnTop):
        if alwaysOnTop:
            NoteManager.ALWAYS_ON_TOP = True
            Note.flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
            if len(NoteManager.notes) > 0:
                NoteManager.cloneNote(NoteManager.notes[0])
        else:
            NoteManager.ALWAYS_ON_TOP = False
            Note.flags = Qt.FramelessWindowHint | Qt.Tool
            for note in NoteManager.notes:
                note.setWindowFlags(Note.flags)
                note.showNote()

    @staticmethod
    def saveNotes():
        logger.error('Saving notes')
        settings = {}
        settings['numNotes'] = len(NoteManager.notes)
        settings['notes'] = []
        for note in NoteManager.notes:
            properties = {}
            properties['geometryX'] = note.geometry().x()
            properties['geometryY'] = note.geometry().y()
            properties['geometryWidth'] = note.geometry().width()
            properties['geometryHeight'] = note.geometry().height()
            properties['text'] = note.editor.toPlainText()
            properties['currentPositionX'] = note.pos().x()
            properties['currentPositionY'] = note.pos().y()
            settings['notes'].append(properties)
        utils.saveSettings(json.dumps(settings))

    @staticmethod
    def loadNotes():
        logger.error('Loading notes')
        stext = utils.loadSettings()
        if not stext:
            stext = '{"numNotes": 0}'
        settings = json.loads(stext)
        if not settings or settings['numNotes'] == 0:
            NoteManager.addNewNote()
        else:
            noteList = settings['notes']
            for n in noteList:
                note = Note()
                note.setGeometry(n['geometryX'], n['geometryY'], n['geometryWidth'], n['geometryHeight'])
                note.editor.setPlainText(n['text'])
                note.showNote()
                note.activateWindow()
                NoteManager.notes.append(note)

    @staticmethod
    def hideAllNotes():
        if not NoteManager.ALWAYS_ON_TOP:
            for note in NoteManager.notes:
                note.hideNote()

    @staticmethod
    def showAllNotes():
        if not NoteManager.ALWAYS_ON_TOP:
            for note in NoteManager.notes:
                note.showNote()




