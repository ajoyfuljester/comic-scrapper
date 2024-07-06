import ConfigUtils
import os
import json


def createLibraryIfDoesNotExist():
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    if not os.path.exists(pathToLibrary):
        os.mkdir(pathToLibrary)


def comicBooks():
    return next(os.walk(ConfigUtils.loadConfig()['PATH_TO_LIBRARY']), [None, []])[1]



blackListedKeys = ['image']
def sanitizeData(data):
    importantData = {}

    for key in data.keys():
        if key not in blackListedKeys:
            importantData[key] = data[key]

    return importantData

def constructDataFile(data):
    return json.dumps(data, indent=4)

    



def addToLibrary(data):
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']

    path = os.path.join(pathToLibrary, data['title'])
    os.mkdir(path)
    with open(os.path.join(path, 'data.json'), 'w') as file:
        file.write(constructDataFile({'info': sanitizeData(data)}))
