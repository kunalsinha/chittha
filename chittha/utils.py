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
