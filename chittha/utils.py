# Chittha - a sticky notes application
# Copyright (C) 2019 Kunal Sinha <kunalsinha4u@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.Qt import QStandardPaths
from PyQt5.QtCore import QDir, QFile, QIODevice, QTextStream
import logging

logger = logging.getLogger(__name__)

def getSettingsFile():
    appPath = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    appDir = QDir(appPath)
    if not appDir.exists():
        logger.debug('Creating app directory')
        appDir.mkpath(appDir.absolutePath())
    else:
        logger.debug('App directory already exists')
    if appDir.setCurrent(appDir.absolutePath()):
        logger.debug('Changing cwd to app data directory')
    else:
        logger.debug('Changing cwd to app data directory failed')
    return QFile('settings.json')

def saveSettings(settings):
    logger.debug('Saving settings')
    currentDir = QDir()
    logger.debug(currentDir.absolutePath())
    settingsFile = getSettingsFile()
    if not settingsFile.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.Truncate):
        logger.debug('Settings file could not be opened for writing')
    else:
        stream = QTextStream(settingsFile)
        stream << settings
        settingsFile.flush()
        settingsFile.close()
    currentDir.setCurrent(currentDir.absolutePath())
    logger.debug('Changing cwd to runtime')

def loadSettings():
    logger.debug('Loading settings')
    currentDir = QDir()
    logger.debug(currentDir.absolutePath())
    settingsFile = getSettingsFile()
    settings = None
    if not settingsFile.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        logger.debug('Settings file could not be opened for reading')
    else:
        stream = QTextStream(settingsFile)
        settings = stream.readAll()
        settingsFile.close()
    currentDir.setCurrent(currentDir.absolutePath())
    logger.debug('Changing cwd to runtime')
    return settings

# returns rgba(r, g, b, a) from QColor
def getRGBA(color):
    red = color.red()
    green = color.green()
    blue = color.blue()
    alpha = color.alpha()
    colorCode = 'rgba('
    colorCode += str(red) + ', ' + str(green) + ', ' + str(blue) + ', ' + str(alpha)
    colorCode += ')'
    return colorCode

