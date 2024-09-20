from . import SettingsUtils
import os
import shutil

def getBooks():
    settings = SettingsUtils.loadSettings()
    return next(os.walk(settings['PATH_TO_LOCAL']), [None, []])[1]


def getIssues(name):
    settings = SettingsUtils.loadSettings()

    path = os.path.join(settings['PATH_TO_LOCAL'], name)

    return sorted(next(os.walk(path), [None, []])[1], reverse=True, key=trimName)

def getBookInfo(bookName):
    data = {
        'info': {
            'title': bookName,
        },
        'issues': [{'name': issue} for issue in getIssues(bookName)],
    }
    
    data['info']['numberOfIssues'] = len(data['issues'])

    return data
    
    

def deleteBook(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LOCAL'], bookName)
    shutil.rmtree(path)

def deleteIssue(bookName, issueName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LOCAL'], bookName, issueName)
    if not os.path.exists(path):
        return
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

prefixes = ['', 'k', 'M', 'G', 'T']
def parseSize(n):
    prefix = 0
    while n >= 1000:
        n = int(n)
        n /= 1000
        prefix += 1
    return f"{n}{prefixes[prefix]}B"

def trimName(name):
    settings = SettingsUtils.loadSettings()
    right = settings['SORT_TRIM_RIGHT']
    if right == 0:
        right = -1 * (len(name) + 1)
    trimmed = name[settings['SORT_TRIM_LEFT']: -1 * right]
    try:
        n = int(trimmed)
        return n
    except ValueError:
        return trimmed
