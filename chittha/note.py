# Chittha - a sticky notes application
# Copyright (C) 2019 Kunal Sinha <kunalsinha4u@gmail.com>
#
# Chittha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chittha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chittha.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.Qt import QStandardPaths
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor, QColor
from PyQt5.QtWidgets import *
from chittha import utils, resources
import json
import logging
from chittha.dllist import DLList

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
        self.resizer = NoteResizer(self)
        self.layout.addWidget(self.resizer)
        # add the layout to the note widget
        self.setLayout(self.layout)
        # register shortcuts
        self.registerShortcuts()
        # mark inactive by default
        self.isActive = False
        # styling
        self.setStyleSheet(NoteManager.getStyleSheet())

    def hideNote(self):
        if not self.isHidden:
            self.currentPosition = self.pos()
        self.hide()
        self.isHidden = True
        logger.debug('Hiding at: ' + str(self.currentPosition))

    def showNote(self):
        self.hide()
        if self.currentPosition:
            self.move(self.currentPosition)
            logger.debug('Moving to: ' + str(self.currentPosition))
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
        self.registerShortcut('Ctrl+H', NoteManager.hideAllNotes)
        self.registerShortcut('Ctrl+S', NoteManager.showAllNotes)
        self.registerShortcut('Ctrl+J', self.focusNextNote)
        self.registerShortcut('Ctrl+K', self.focusPrevNote)
        self.registerShortcut('Ctrl+L', self.menu.lockNote)
        self.registerShortcut('Ctrl+P', NoteManager.toggleAlwaysOnTop2)

    def registerShortcut(self, sequence, handler):
        shortcut = QShortcut(QKeySequence(sequence), self)
        shortcut.activated.connect(handler)

    def focusNextNote(self):
        NoteManager.focusNote(self.next)

    def focusPrevNote(self):
        NoteManager.focusNote(self.prev)

class NoteMenu(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # create a horizontal layout for the top menu
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 5, 2)
        # add a new note button
        self.new = self.buttonFactory(resources.getResourcePath('new.png'), None, self.createNewNote)
        self.new.setToolTip('Create new note')
        self.layout.addWidget(self.new)
        # add a lock note button
        self.lock = self.buttonFactory(resources.getResourcePath('unlock.png'), None, self.lockNote)
        self.lock.setToolTip('Unlocked')
        self.layout.addWidget(self.lock)
        # add empty space
        self.layout.addStretch(1)
        # add a delete note button
        self.delete = self.buttonFactory(resources.getResourcePath('delete.png'), None, self.deleteNote)
        self.delete.setToolTip('Delete note')
        self.layout.addWidget(self.delete)

    def buttonFactory(self, icon, text, handler):
        button = QPushButton(QIcon(icon), text, self)
        button.clicked.connect(handler)
        return button

    def lockNote(self):
        self.parentWidget().lockNote()
        if self.parentWidget().editor.isReadOnly():
            self.lock.setIcon(QIcon(resources.getResourcePath('lock.png')))
            self.lock.setToolTip('Locked')
        else:
            self.lock.setIcon(QIcon(resources.getResourcePath('unlock.png')))
            self.lock.setToolTip('Unlocked')

    def createNewNote(self):
        NoteManager.addNewNote()

    def deleteNote(self):
        self.parentWidget().deleteNote()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.isLeftMouseButtonPressed = True
            self.startPosition = self.mapToGlobal(event.pos())
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isLeftMouseButtonPressed:
            self.endPosition = self.mapToGlobal(event.pos())
            self.delta = self.endPosition - self.startPosition
            self.newPosition = self.mapToGlobal(self.delta)
            self.parentWidget().setGeometry(self.newPosition.x(), self.newPosition.y(), self.parentWidget().width(), self.parentWidget().height())
            self.startPosition = self.endPosition
            self.parentWidget().currentPosition = self.newPosition

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.isLeftMouseButtonPressed:
            self.isLeftMouseButtonPressed = False
            self.setCursor(Qt.ArrowCursor)

class NoteEditor(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursorWidth(2)
        self.setFrameStyle(QFrame.NoFrame)
        if NoteManager.font:
            self.setFont(NoteManager.font)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        NoteManager.markActive(self.parentWidget())

class NoteResizer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(1)
        grip = QSizeGrip(self)
        image = resources.getResourcePath('resizer.png')
        grip.setStyleSheet('background-image: url({0});'.format(image))
        self.layout.addWidget(grip)

class NoteManager:

    notes = DLList()
    alwaysOnTop = False
    bgColor = None
    textColor = None
    font = None

    @staticmethod
    def addNewNote():
        note = Note()
        note.showNote()
        note.editor.setFocus()
        NoteManager.notes.add(note)

    @staticmethod
    def deleteNote(note):
        if note in NoteManager.notes.all():
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
        NoteManager.notes.add(clone)

    @staticmethod
    def toggleAlwaysOnTop(alwaysOnTop):
        if alwaysOnTop:
            NoteManager.alwaysOnTop = True
            Note.flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
            if NoteManager.notes.length() > 0:
                NoteManager.cloneNote(NoteManager.notes.head)
        else:
            NoteManager.alwaysOnTop = False
            Note.flags = Qt.FramelessWindowHint | Qt.Tool
            for note in NoteManager.notes.all():
                note.setWindowFlags(Note.flags)
                note.showNote()

    @staticmethod
    def toggleAlwaysOnTop2():
        NoteManager.toggleAlwaysOnTop(not NoteManager.alwaysOnTop)

    @staticmethod
    def saveNotes():
        logger.debug('Saving notes')
        settings = {}
        settings['numNotes'] = NoteManager.notes.length()
        settings['notes'] = []
        for note in NoteManager.notes.all():
            properties = {}
            properties['geometryX'] = note.geometry().x()
            properties['geometryY'] = note.geometry().y()
            properties['geometryWidth'] = note.geometry().width()
            properties['geometryHeight'] = note.geometry().height()
            properties['text'] = note.editor.toPlainText()
            properties['currentPositionX'] = note.pos().x()
            properties['currentPositionY'] = note.pos().y()
            properties['isActive'] = note.isActive
            settings['notes'].append(properties)
        utils.saveSettings(json.dumps(settings))

    @staticmethod
    def loadNotes():
        logger.debug('Loading notes')
        stext = utils.loadSettings()
        if not stext:
            stext = '{"numNotes": 0}'
        settings = json.loads(stext)
        if not settings or settings['numNotes'] == 0:
            NoteManager.addNewNote()
        else:
            noteList = settings['notes']
            activeNote = None
            for n in noteList:
                note = Note()
                note.setGeometry(n['geometryX'], n['geometryY'], n['geometryWidth'], n['geometryHeight'])
                note.editor.setPlainText(n['text'])
                note.editor.moveCursor(QTextCursor.End)
                NoteManager.notes.add(note)
                if n['isActive'] == True:
                    activeNote = note
                    continue
                note.showNote()
            if activeNote:
                activeNote.showNote()
                activeNote.editor.setFocus()

    @staticmethod
    def hideAllNotes():
        if not NoteManager.alwaysOnTop:
            for note in NoteManager.notes.all():
                note.hideNote()

    @staticmethod
    def showAllNotes():
        if not NoteManager.alwaysOnTop:
            activeNote = None
            for note in NoteManager.notes.all():
                if note.isActive:
                    activeNote = note
            for note in NoteManager.notes.all():
                if note == activeNote:
                    continue
                note.showNote()
            if activeNote:
                activeNote.showNote()
                activeNote.editor.setFocus()

    @staticmethod
    def focusNote(note):
        note.showNote()
        note.editor.setFocus()

    @staticmethod
    def markActive(note):
        for n in NoteManager.notes.all():
            n.isActive = False
            n.menu.setStyleSheet('background-color: ' + utils.getRGBA(NoteManager.bgColor) + ';')
        note.isActive = True
        note.menu.setStyleSheet('background-color: ' + utils.getLighterRGBA(NoteManager.bgColor) + ';')

    @staticmethod
    def getStyleSheet():
        stylesheet = ''
        bgColorCode = utils.getRGBA(NoteManager.bgColor)
        stylesheet += 'background-color: ' + bgColorCode + '; '
        textColorCode = utils.getRGBA(NoteManager.textColor)
        stylesheet += 'color: ' + textColorCode + '; '
        return stylesheet

    @staticmethod
    def updateBgColor(color):
        NoteManager.bgColor = color
        for note in NoteManager.notes.all():
            note.setStyleSheet(NoteManager.getStyleSheet())
            if note.isActive:
                note.menu.setStyleSheet('background-color: ' + utils.getLighterRGBA(NoteManager.bgColor) + ';')
            else:
                note.menu.setStyleSheet('background-color: ' + utils.getRGBA(NoteManager.bgColor) + ';')

    @staticmethod
    def updateTextColor(color):
        NoteManager.textColor = color
        for note in NoteManager.notes.all():
            note.setStyleSheet(NoteManager.getStyleSheet())

    @staticmethod
    def updateOpacity(opacity):
        NoteManager.opacity = opacity
        for note in NoteManager.notes.all():
            note.setStyleSheet(NoteManager.getStyleSheet())

    @staticmethod
    def updateFont(font):
        NoteManager.font = font
        for note in NoteManager.notes.all():
            note.editor.setFont(font)

