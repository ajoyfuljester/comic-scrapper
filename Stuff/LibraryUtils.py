from . import ConfigUtils
import os
import shutil
import json
from . import ScrapingUtils
from threading import Thread

def forceFilename(name):
    return "".join([c if c not in r':?\/"*<>|' else "_" for c in name])

def createLibraryIfDoesNotExist():
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    if not os.path.exists(pathToLibrary):
        os.mkdir(pathToLibrary)


def getBooks():
    config = ConfigUtils.loadConfig()
    books = next(os.walk(config['PATH_TO_LIBRARY']), [None, []])[1]
    return list(filter(lambda book: os.path.exists(os.path.join(config['PATH_TO_LIBRARY'], book, 'data.json')), books))


def getBookInfo(name):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(name), 'data.json')

    with open(path, 'r') as file:
        data = json.loads(file.read())
        data['info']['image'] = bytes.fromhex(data['info']['image'])
        return data


blackListedKeys = ['image']
def truncateData(data, blacklist = blackListedKeys):
    importantData = {}

    for key in data.keys():
        if key not in blacklist:
            importantData[key] = data[key]

    return importantData

def constructJSON(data):
    return json.dumps(data, indent=4)



def addToLibrary(url):
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    info = ScrapingUtils.getFullComicBookInfo(url)

    path = os.path.join(pathToLibrary, forceFilename(info['info']['title']))
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, 'data.json'), 'w') as file:
        file.write(constructJSON(info))
    with open(os.path.join(path, 'progress.json'), 'w') as file:
        for i in info['issues']:
            i['isRead'] = False
        file.write(constructJSON(info['issues']))


def getDownloadedIssues(name):
    config = ConfigUtils.loadConfig()

    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(name))

    return next(os.walk(path), [None, []])[1]


def downloadIssue(title, info, imageNames = None, after = lambda: None, afterArgs = []):
    config = ConfigUtils.loadConfig()
    url = info['URL']
    if url[-5:] != '/full':
        url += '/full'
    sources = ScrapingUtils.getSources(url)
    ScrapingUtils.saveSources(sources, os.path.join(config['PATH_TO_LIBRARY'], forceFilename(title), forceFilename(info['name'])), imageNames)
    try:
        after(*afterArgs)
    except RuntimeError as _:
        pass

def downloadIssueAsThread(title, info, imageNames = None, after = lambda: None, afterArgs = []):
    thread = Thread(target=downloadIssue, args=(title, info, imageNames, after, afterArgs))
    thread.start()


def getIssuePagesPaths(title, issue):
    config = ConfigUtils.loadConfig()

    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(title), forceFilename(issue))

    return [os.path.join(path, p) for p in sorted(next(os.walk(path), [None, None, []])[2], key=lambda x: int(x[:-4]))]

def getReadingProgress(bookName):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(bookName), 'progress.json')
    with open(path, 'r') as file:
        return json.loads(file.read())


def markIssueReadingProgress(bookName, issueName, isRead = True):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(bookName), 'progress.json')
    progress = getReadingProgress(bookName)
    index = [i['name'] for i in progress].index(issueName)
    progress[index]['isRead'] = isRead
    with open(path, 'w') as file:
        file.write(constructJSON(progress))

def deleteIssue(bookName, issueName):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(bookName), forceFilename(issueName))
    if not os.path.exists(path):
        return
    shutil.rmtree(path)


def deleteBook(bookName):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], forceFilename(bookName))
    shutil.rmtree(path)
