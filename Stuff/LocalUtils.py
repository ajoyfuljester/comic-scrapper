from . import SettingsUtils
import os

def getBooks():
    settings = SettingsUtils.loadSettings()
    return next(os.walk(settings['PATH_TO_LOCAL']), [None, []])[1]


