from PySide6 import QtWidgets
import LibraryUtils
from QtUtils import *


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        LibraryUtils.createLibraryIfDoesNotExist()


        self.gridLayout = QtWidgets.QGridLayout(self)
        
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText('Type here to search')
        self.gridLayout.addWidget(self.search, 0, 0)

        self.comicBookContainer = QtWidgets.QTableWidget()
        self.comicBookContainer.setColumnCount(1)
        self.comicBookContainer.setHorizontalHeaderLabels(['Title'])
        tableHeaders = self.comicBookContainer.horizontalHeader()
        tableHeaders.setSectionResizeMode(0, ResizeMode.Stretch)
        self.gridLayout.addWidget(self.comicBookContainer, 1, 0)
        
        comicBooks = LibraryUtils.comicBooks()

        for cb in comicBooks:
            rowCount = self.comicBookContainer.rowCount()
            self.comicBookContainer.setRowCount(rowCount + 1)
            self.comicBookContainer.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(cb))
