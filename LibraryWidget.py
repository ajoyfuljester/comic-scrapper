from PySide6 import QtWidgets
from ConfigUtils import loadConfig
import os





class LibraryWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.config = loadConfig()

        pathToComicBooks = self.config['PATH_TO_COMIC_BOOKS']
        comicBookPathExists = os.path.exists(pathToComicBooks)
        if self.config['CREATE_DIR_IF_DOES_NOT_EXIST'] and not comicBookPathExists:
            os.mkdir(pathToComicBooks)
        
        downloadedComics = next(os.walk(pathToComicBooks))[1]
