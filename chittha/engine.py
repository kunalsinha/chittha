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

from PyQt5.QtCore import QPoint, QTimer, QSettings, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
from chittha.note import NoteManager
from chittha.settings import Ui_Settings
from chittha.about import Ui_TabWidget
from chittha import resources
import logging
import signal

logger = logging.getLogger(__name__)

class Engine:

    app = None
    settingsDialog = None
    aboutDialog = None
    settings = None

    @staticmethod
    def start():
        Engine.app = QApplication([])
        Engine.app.setOrganizationName('curiousforcode');
        Engine.app.setOrganizationDomain('curiousforcode.com');
        Engine.app.setApplicationName('chittha');
        Engine.app.aboutToQuit.connect(Engine.stop)
        # save notes every five seconds
        Engine.scheduleNoteSaver()
        # application settings
        Engine.settings = QSettings()
        # load application settings
        Engine.loadSettings()
        # initialize settings dialog
        Engine.settingsDialog = QDialog()
        ui_settings = Ui_Settings()
        ui_settings.setupUi(Engine.settingsDialog)
        # Initialize about dialog
        Engine.aboutDialog = QTabWidget()
        ui_about = Ui_TabWidget()
        ui_about.setupUi(Engine.aboutDialog)
        # system tray
        Engine.createSystemTray()
        # load saved notes
        Engine.loadNotes() # load saved notes
        Engine.app.setQuitOnLastWindowClosed(False)
        Engine.app.exec_()

    @staticmethod
    def createSystemTray():
        if QSystemTrayIcon.isSystemTrayAvailable:
            tray = QSystemTrayIcon(Engine.app)
            # set the tray icon
            trayIcon =  QIcon(resources.getResourcePath('tray-icon.png'))
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
        Engine.saveSettings()

    @staticmethod
    def scheduleNoteSaver():
        logger.debug('Scheduled note saver')
        timer = QTimer(Engine.app)
        timer.timeout.connect(NoteManager.saveNotes)
        timer.start(5000)

    @staticmethod
    def loadNotes():
        NoteManager.loadNotes()

    @staticmethod
    def saveSettings():
        logger.error('Saving settings')
        Engine.settings.setValue('bgColor', NoteManager.bgColor)
        Engine.settings.setValue('textColor', NoteManager.textColor)
        if NoteManager.font:
            Engine.settings.setValue('font', NoteManager.font)
        Engine.settings.sync()

    @staticmethod
    def loadSettings():
        logger.error('Loading settings')
        NoteManager.bgColor = Engine.settings.value('bgColor', QColor(Qt.yellow), QColor)
        NoteManager.textColor = Engine.settings.value('textColor', QColor(Qt.black), QColor)
        if Engine.settings.contains('font'):
            NoteManager.font = Engine.settings.value('font')

class TrayMenu(QMenu):

    def __init__(self):
        super().__init__()
        self.addItem('New Note', False, self.createNewNote)
        self.addSeparator()
        self.showAll = self.addItem('Show All', False, self.showAllNotes)
        self.hideAll = self.addItem('Hide All', False, self.hideAllNotes)
        self.alwaysOnTop = self.addItem('Always On Top', True, self.toggleAlwaysOnTop)
        self.addSeparator()
        self.settings = self.addItem('Settings', False, self.showSettings)
        self.about = self.addItem('About', False, self.showAbout)
        self.addItem('Quit', False, self.quit)

    def addItem(self, label, isCheckable, handler):
        action = self.addAction(label)
        action.setCheckable(isCheckable)
        action.triggered.connect(handler)
        return action

    def createNewNote(self):
        NoteManager.addNewNote()
    
    def hideAllNotes(self):
        NoteManager.hideAllNotes()

    def showAllNotes(self):
        NoteManager.showAllNotes()

    def showSettings(self):
        Engine.settingsDialog.show()

    def showAbout(self):
        Engine.aboutDialog.show()

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

