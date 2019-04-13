from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from chittha.note import Note, NoteManager
import signal

class Engine:

    app = None
    TRAY_ICON = 'resources/tray-icon.svg'

    @staticmethod
    def start():
        Engine.app = QApplication([])
        Engine.app.setOrganizationName('curiousforcode');
        Engine.app.setOrganizationDomain('curiousforcode.com');
        Engine.app.setApplicationName('chittha');
        Engine.app.aboutToQuit.connect(Engine.stop)
        Engine.createSystemTray()
        NoteManager.loadNotes()
        Engine.app.exec_()

    @staticmethod
    def createSystemTray():
        if QSystemTrayIcon.isSystemTrayAvailable:
            tray = QSystemTrayIcon(Engine.app)
            # set the tray icon
            trayIcon =  QIcon(Engine.TRAY_ICON)
            tray.setIcon(trayIcon)
            # set context menu
            trayMenu = TrayMenu()
            tray.setContextMenu(trayMenu)
            # show initialization message
            message = 'Chittha is running'
            tray.showMessage('Chittha', message)
            # show the tray
            tray.show()

    @staticmethod
    def stop():
        NoteManager.saveNotes()

class TrayMenu(QMenu):

    def __init__(self):
        super().__init__()
        self.addItem('New Note', False, self.createNewNote)
        self.addSeparator()
        self.showAll = self.addItem('Show All', False, self.showAllNotes)
        self.hideAll = self.addItem('Hide All', False, self.hideAllNotes)
        self.addSeparator()
        self.alwaysOnTop = self.addItem('Always On Top', True, self.toggleAlwaysOnTop)
        self.addSeparator()
        self.addItem('Quit', False, self.quit)

    def addItem(self, label, isCheckable, handler):
        action = self.addAction(label)
        action.setCheckable(isCheckable)
        action.triggered.connect(handler)
        return action

    def createNewNote(self):
        NoteManager.addNewNote()
    
    def hideAllNotes(self):
        if not NoteManager.ALWAYS_ON_TOP:
            for note in NoteManager.notes:
                note.hideNote()

    def showAllNotes(self):
        if not NoteManager.ALWAYS_ON_TOP:
            for note in NoteManager.notes:
                note.showNote()

    def quit(self):
        Engine.app.quit()

    def toggleAlwaysOnTop(self):
        isAlwaysOnTop = self.alwaysOnTop.isChecked()
        if isAlwaysOnTop:
            self.showAll.setDisabled(True)
            self.hideAll.setDisabled(True)
        else:
            self.showAll.setDisabled(False)
            self.hideAll.setDisabled(False)
        NoteManager.toggleAlwaysOnTop(isAlwaysOnTop)

