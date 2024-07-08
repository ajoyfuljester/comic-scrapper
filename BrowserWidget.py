from PySide6 import QtWidgets, QtGui
import LibraryUtils
import ScrapingUtils as SU
from QtUtils import *
from GenericWidgets import ComicPreview

class BrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText('Type here to search')
        self.search.returnPressed.connect(self.searchComics)

        self.results = QtWidgets.QTableWidget()
        self.results.setColumnCount(4)
        self.results.setHorizontalHeaderLabels(['Title', 'Status', 'Release Year', 'Latest Issue'])
        tableHeader = self.results.horizontalHeader()
        tableHeader.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(2, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(3, ResizeMode.Stretch)


        self.results.itemSelectionChanged.connect(self.handleItemClick)

        self.comicData = []

        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout.addWidget(self.search, 0, 0)
        self.gridLayout.addWidget(self.results, 1, 0)

        self.addToLibraryButton = QtWidgets.QPushButton()
        self.addToLibraryButton.setText('Add to library')
        self.addToLibraryButton.clicked.connect(self.addSelectedToLibrary)
        self.gridLayout.addWidget(self.addToLibraryButton, 0, 1)


    def searchComics(self):
        query = self.search.text()

        self.comicData = SU.search(query)

        entryWidgets = [ComicTableWidgetItemSet(entry) for entry in self.comicData]
        self.results.setRowCount(0)

        for entryWidget in entryWidgets:
            entryWidget.appendSelf(self.results)

    def loadPreview(self, data):
        self.preview = ComicPreview(data)
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.gridLayout.addWidget(self.preview, 1, 1)
        self.preview.show()

        
        size = self.preview.coverLabel.frameSize()
        self.preview.resizeCover(size)



    def handleItemClick(self):
        indexes = self.results.selectedIndexes()
        if len(indexes) > 0:
            row = indexes[0].row()
            data = self.comicData[row]
            self.loadPreview(data)
    

    def addSelectedToLibrary(self):
        selectedIndexes = set([index.row() for index in self.results.selectedIndexes()])
        selectedComicBooks = [self.comicData[i] for i in selectedIndexes]
        for cb in selectedComicBooks:
            LibraryUtils.addToLibrary(cb)
        
        

class ComicTableWidgetItemSet():
    defaultBackground = 'white'
    highlightBackground = 'lightgray'
    def __init__(self, entry):

        self.cellData = [
            entry['title'],
            entry['status'],
            entry['releaseYear'],
            entry['latest'],
        ]

        self.cellWidgets = [QtWidgets.QTableWidgetItem(cell) for cell in self.cellData]
        highlight = self.cellData[0] in LibraryUtils.comicBooks()
        for cell in self.cellWidgets:
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(QtGui.QBrush(self.highlightBackground if highlight else self.defaultBackground))

    
    def appendSelf(self, target):
        lastRow = target.rowCount()
        target.setRowCount(lastRow + 1)
        for i, cell in enumerate(self.cellWidgets):
            target.setItem(lastRow, i, cell)
