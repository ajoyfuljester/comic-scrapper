from shutil import Error
from . import SettingsUtils
import os
import json
import shutil

def getBooks():
    settings = SettingsUtils.loadSettings()
    return next(os.walk(settings['PATH_TO_LOCAL']), [None, []])[1]


def getIssues(name):
    settings = SettingsUtils.loadSettings()

    path = os.path.join(settings['PATH_TO_LOCAL'], name)

    return next(os.walk(path), [None, []])[1]

def _getReadingProgress(bookName): # i'm not sure about this, this would mean, that Local widget would be invasive
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LOCAL'], bookName, 'progress.json')
    with open(path, 'r') as file:
        return json.loads(file.read())

def _getBookInfo(bookName):
    info = {}
    raise Error('DO THIS LATER (AFTER I DO OTHER FUNCTIONS) (REMEMBER TO DELETE UNDERSCORE FROM THE NAME)')
    

def deleteBook(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LOCAL'], bookName)
    shutil.rmtree(path)

def getBookSize(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LOCAL'], bookName)
    size = 0
    for dirpath, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(dirpath, file)
            size += os.path.getsize(filepath)

    return size
