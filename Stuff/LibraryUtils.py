from sys import settrace
from . import SettingsUtils
import os
import shutil
import json
from . import ScrapingUtils
from threading import Thread
import rapidfuzz

def forceFilename(name):
    return "".join([c if c not in r':?\/"*<>|' else "_" for c in name])

def createLibraryIfDoesNotExist():
    settings = SettingsUtils.loadSettings()

    pathToLibrary = settings['PATH_TO_LIBRARY']
    if not os.path.exists(pathToLibrary):
        os.mkdir(pathToLibrary)


def getBooks():
    settings = SettingsUtils.loadSettings()
    books = next(os.walk(settings['PATH_TO_LIBRARY']), [None, []])[1]
    return list(filter(lambda book: os.path.exists(os.path.join(settings['PATH_TO_LIBRARY'], book, 'data.json')), books))


def getBookInfo(name):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(name), 'data.json')

    with open(path, 'r') as file:
        data = json.loads(file.read())
        if data['info'].get('image') != None:
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



def addToLibrary(url, selector = None, innerSelector = None, urlSuffix = ''):
    settings = SettingsUtils.loadSettings()

    pathToLibrary = settings['PATH_TO_LIBRARY']
    info = ScrapingUtils.getFullComicBookInfo(url, selector)
    info['info']['innerSelector'] = innerSelector

    for issue in info['issues']:
        issue['URL'] += urlSuffix

    path = os.path.join(pathToLibrary, forceFilename(info['info']['title']))
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, 'data.json'), 'w') as file:
        file.write(constructJSON(info))
    with open(os.path.join(path, 'progress.json'), 'w') as file:
        for i in info['issues']:
            i['isRead'] = False
        file.write(constructJSON(info['issues']))

    return True

def updateBook(url):
    settings = SettingsUtils.loadSettings()

    pathToLibrary = settings['PATH_TO_LIBRARY']
    data = ScrapingUtils.getFullComicBookInfo(url)

    path = os.path.join(pathToLibrary, forceFilename(data['info']['title']))
    if not os.path.exists(path):
        os.mkdir(path)

    with open(os.path.join(path, 'data.json'), 'r') as file:
        old = json.loads(file.read())

    with open(os.path.join(path, 'data.json'), 'w') as file:
        file.write(constructJSON(old | data))

    old = getReadingProgress(data['info']['title'])
    with open(os.path.join(path, 'progress.json'), 'w') as file:
        read = [issue['name'] for issue in old if issue['isRead']]
        for i in data['issues']:
            i['isRead'] = i['name'] in read
        file.write(constructJSON(data['issues']))


def getDownloadedIssues(name):
    settings = SettingsUtils.loadSettings()

    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(name))

    return next(os.walk(path), [None, []])[1]


def downloadIssue(title, info, innerSelector = None, imageNames = None, after = lambda: None, afterArgs = []):
    settings = SettingsUtils.loadSettings()
    url = info['URL']
    if url[-5:] != '/full' and innerSelector == None:
        url += '/full'

    sources = ScrapingUtils.getSources(url, None, innerSelector)
    ScrapingUtils.saveSources(sources, os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(title), forceFilename(info['name'])), imageNames)
    try:
        after(*afterArgs)
    except RuntimeError as _:
        pass

def downloadIssueAsThread(title, info, innerSelector = None, imageNames = None, after = lambda: None, afterArgs = []):
    thread = Thread(target=downloadIssue, args=(title, info, innerSelector, imageNames, after, afterArgs))
    thread.start()


def getIssuePagesPaths(title, issue):
    settings = SettingsUtils.loadSettings()

    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(title), forceFilename(issue))

    return [os.path.join(path, p) for p in sorted(next(os.walk(path), [None, None, []])[2], key=lambda x: int(x[:-4]))]

def getReadingProgress(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(bookName), 'progress.json')
    with open(path, 'r') as file:
        return json.loads(file.read())


def markIssueReadingProgress(bookName, issueName, isRead = True):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(bookName), 'progress.json')
    progress = getReadingProgress(bookName)
    index = [i['name'] for i in progress].index(issueName)
    progress[index]['isRead'] = isRead
    with open(path, 'w') as file:
        file.write(constructJSON(progress))

def deleteIssue(bookName, issueName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(bookName), forceFilename(issueName))
    if not os.path.exists(path):
        return
    shutil.rmtree(path)


def deleteBook(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(bookName))
    shutil.rmtree(path)

def getBookSize(bookName):
    settings = SettingsUtils.loadSettings()
    path = os.path.join(settings['PATH_TO_LIBRARY'], forceFilename(bookName))
    size = 0
    for dirpath, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(dirpath, file)
            size += os.path.getsize(filepath)

    return size


prefixes = ['', 'k', 'M', 'G', 'T', 'P', 'Y', 'Z']
def parseSize(n):
    prefix = 0
    while n >= 1000:
        n = int(n)
        n /= 1000
        prefix += 1
    return f"{n}{prefixes[prefix]}B"



def createList(url, outerSelector, selector, innerSelector, urlSuffix):
    books = ScrapingUtils.getBooks(url, outerSelector)
    l = {
        "selector": selector,
        "innerSelector": innerSelector,
        "urlSuffix": urlSuffix,
        "books": books,
    }

    j = constructJSON(l)


    settings = SettingsUtils.loadSettings()

    path = settings["PATHNAME_TO_LIST"]

    with open(path, 'w') as file:
        file.write(j)

    return True

    
def loadList():
    settings = SettingsUtils.loadSettings()
    path = settings["PATHNAME_TO_LIST"]

    j = ''

    with open(path, 'r') as file:
        j = file.read()

    l = json.loads(j)

    return l

def searchList(query, limit):
    l = loadList()
    books = l["books"]
    if limit <= 0:
        limit = len(books)

    titles = {i: book['title'] for i, book in enumerate(books)}

    results = rapidfuzz.process.extract(query, titles, scorer=rapidfuzz.fuzz.partial_ratio, limit=limit)

    sortedBooks = [books[r[2]] for r in results]

    return sortedBooks

