import ConfigUtils
import os
import json
import ScrapingUtils


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

    print('NOT RETURNING', path)
    raise Exception('IDK what this function was supposed to be for')


def downloadIssue(comicBookName, info, imageNames = None):
    config = ConfigUtils.loadConfig()
    url = info['URL']
    if url[-5:] != '/full':
        url += '/full'
    sources = ScrapingUtils.getSources(url)
    ScrapingUtils.saveSources(sources, os.path.join(config['PATH_TO_LIBRARY'], comicBookName, info['name']), imageNames)
