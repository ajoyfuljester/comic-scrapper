import ConfigUtils
import os


def libraryExists():
    return os.path.exists(ConfigUtils.loadConfig()['PATH_TO_LIBRARY'])


def createLibraryIfDoesNotExist():
    config = ConfigUtils.loadConfig()

    pathToLibrary = config['PATH_TO_LIBRARY']
    if config['CREATE_LIBRARY_IF_DOES_NOT_EXIST'] and not libraryExists():
        os.mkdir(pathToLibrary)


def comicBooks():
    return next(os.walk(ConfigUtils.loadConfig()['PATH_TO_LIBRARY']))[1]
