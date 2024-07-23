from PySide6 import QtWidgets, QtGui
from . import LibraryUtils
from . import ScrapingUtils
from .QtUtils import *
from .GenericWidgets import ComicPreviewWidget
from . import ConfigUtils

class BrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.returnPressed.connect(self.searchComics)

        self.searchResultContainer = QtWidgets.QTableWidget()
        self.searchResultContainer.setColumnCount(4)
        self.searchResultContainer.setHorizontalHeaderLabels(['Title', 'Status', 'Release Year', 'Latest Issue'])
        tableHeader = self.searchResultContainer.horizontalHeader()
        tableHeader.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(2, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(3, ResizeMode.Stretch)


        self.searchResultContainer.itemSelectionChanged.connect(self.handleSelectionChange)

        self.bookData = []

        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout.addWidget(self.searchInput, 0, 0)
        self.gridLayout.addWidget(self.searchResultContainer, 1, 0)

        self.addToLibraryButton = QtWidgets.QPushButton()
        self.addToLibraryButton.setText('Add to library')
        self.addToLibraryButton.clicked.connect(self.addSelectedToLibrary)
        self.gridLayout.addWidget(self.addToLibraryButton, 0, 1)


    def searchComics(self):
        query = self.searchInput.text()

        self.bookData = ScrapingUtils.search(query)

        rowWidgets = [ComicTableWidgetItemSet(entry) for entry in self.bookData]
        self.searchResultContainer.setRowCount(0)

        for rowWidget in rowWidgets:
            rowWidget.appendSelf(self.searchResultContainer)

    def showPreview(self, data):
        self.preview = ComicPreviewWidget(data)
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.gridLayout.addWidget(self.preview, 1, 1)



    def handleSelectionChange(self):
        indexes = self.searchResultContainer.selectedIndexes()
        if len(indexes) > 0:
            row = indexes[0].row()
            data = self.bookData[row]
            self.showPreview(data)
    

    def addSelectedToLibrary(self):
        selectedIndexes = set([index.row() for index in self.searchResultContainer.selectedIndexes()])
        selectedComicBooks = [self.bookData[i] for i in selectedIndexes]

        
        for cb in selectedComicBooks:
            LibraryUtils.addToLibrary(cb['URL'])
        
        
class ComicTableWidgetItemSet():
    defaultBackground = 'white'
    def __init__(self, details):
        self.highlightBackground = ConfigUtils.loadConfig()['COLOR_BOOK_ALREADY_IN_LIBRARY']

        self.cellData = [
            details['title'],
            details['status'],
            details['releaseYear'],
            details['latest'],
        ]


        self.cellWidgets = [QtWidgets.QTableWidgetItem(cell) for cell in self.cellData]
        highlight = LibraryUtils.forceFilename(self.cellData[0]) in LibraryUtils.getBooks()
        brush = QtGui.QBrush(self.highlightBackground if highlight else self.defaultBackground)
        for cell in self.cellWidgets:
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(brush)

    
    def appendSelf(self, target):
        lastRow = target.rowCount()
        target.setRowCount(lastRow + 1)
        for i, cell in enumerate(self.cellWidgets):
            target.setItem(lastRow, i, cell)