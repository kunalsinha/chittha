from PyQt5.Qt import QStandardPaths
from PyQt5.QtCore import QDir, QFile, QIODevice, QTextStream
import logging

logger = logging.getLogger(__name__)

def getSettingsFile():
    appPath = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    appDir = QDir(appPath)
    if not appDir.exists():
        logger.error('Creating app directory')
        appDir.mkpath(appDir.absolutePath())
    else:
        logger.error('App directory already exists')
    if appDir.setCurrent(appDir.absolutePath()):
        logger.error('Changing cwd to app data directory')
    else:
        logger.error('Changing cwd to app data directory failed')
    return QFile('settings.json')

def saveSettings(settings):
    logger.error('Saving settings')
    currentDir = QDir()
    logger.error(currentDir.absolutePath())
    settingsFile = getSettingsFile()
    if not settingsFile.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.Truncate):
        logger.error('Settings file could not be opened for writing')
    else:
        stream = QTextStream(settingsFile)
        stream << settings
        settingsFile.flush()
        settingsFile.close()
    currentDir.setCurrent(currentDir.absolutePath())
    logger.error('Changing cwd to runtime')

def loadSettings():
    logger.error('Loading settings')
    currentDir = QDir()
    logger.error(currentDir.absolutePath())
    settingsFile = getSettingsFile()
    settings = None
    if not settingsFile.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        logger.error('Settings file could not be opened for reading')
    else:
        stream = QTextStream(settingsFile)
        settings = stream.readAll()
        settingsFile.close()
    currentDir.setCurrent(currentDir.absolutePath())
    logger.error('Changing cwd to runtime')
    return settings
