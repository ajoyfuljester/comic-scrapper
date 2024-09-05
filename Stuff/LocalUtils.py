from . import SettingsUtils
import os

def getBooks():
    settings = SettingsUtils.loadSettings()
    return next(os.walk(settings['PATH_TO_LOCAL']), [None, []])[1]


def getIssues(name):
    settings = SettingsUtils.loadSettings()

    path = os.path.join(settings['PATH_TO_LOCAL'], name)

    return next(os.walk(path), [None, []])[1]
