import ConfigUtils
import os
import json
import ScrapingUtils
from threading import Thread


def createLibraryIfDoesNotExist():
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    if not os.path.exists(pathToLibrary):
        os.mkdir(pathToLibrary)


def getComicBooks():
    return next(os.walk(ConfigUtils.loadConfig()['PATH_TO_LIBRARY']), [None, []])[1]


def getComicBookInfo(name):
    config = ConfigUtils.loadConfig()
    path = os.path.join(config['PATH_TO_LIBRARY'], name, 'data.json')

    with open(path, 'r') as file:
        return json.loads(file.read())


blackListedKeys = ['image']
def truncateData(data, blacklist = blackListedKeys):
    importantData = {}

    for key in data.keys():
        if key not in blacklist:
            importantData[key] = data[key]

    return importantData

def constructDataJSON(data):
    return json.dumps(data, indent=4)



def addToLibrary(url):
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    info = ScrapingUtils.getFullComicBookInfo(url)

    path = os.path.join(pathToLibrary, info['info']['title'])
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, 'data.json'), 'w') as file:
        file.write(constructDataJSON(info))


def getDownloadedComicBookIssues(name):
    config = ConfigUtils.loadConfig()

    path = os.path.join(config['PATH_TO_LIBRARY'], name)

    return next(os.walk(path), [None, []])[1]



def getIssuePaths(name, number):
    config = ConfigUtils.loadConfig()

    path = os.path.join(config['PATH_TO_LIBRARY'], name, number)

    raise Exception('IDK what this function was supposed to be for')


def downloadIssue(title, info, imageNames = None, after = lambda: None, afterArgs = []):
    config = ConfigUtils.loadConfig()
    url = info['URL']
    if url[-5:] != '/full':
        url += '/full'
    sources = ScrapingUtils.getSources(url)
    ScrapingUtils.saveSources(sources, os.path.join(config['PATH_TO_LIBRARY'], title, info['name']), imageNames)
    after(*afterArgs)

def downloadIssueAsThread(title, info, imageNames = None, after = lambda: None, afterArgs = []):
    thread = Thread(target=downloadIssue, args=(title, info, imageNames, after, afterArgs))
    thread.start()


def getIssuePages(title, issue):
    config = ConfigUtils.loadConfig()

    path = os.path.join(config['PATH_TO_LIBRARY'], title, issue)

    return [os.path.join(path, p) for p in sorted(next(os.walk(path), [None, None, []])[2], key=lambda x: int(x[:-4]))]
