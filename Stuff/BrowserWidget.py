from PySide6 import QtWidgets, QtGui
from . import LibraryUtils
from . import ScrapingUtils
from .QtUtils import *
from .GenericWidgets import ComicPreviewWidget
from . import ConfigUtils
from Stuff import GenericWidgets

class BrowserWidget(QtWidgets.QWidget):
    defaultStylesheet = 'color: black;'
    highlightStylesheet = 'color: green;'
    def __init__(self):
        super().__init__()
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.setToolTip('Type here to search, press Enter to confirm')
        self.searchInput.returnPressed.connect(self.searchBooks)

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

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.gridLayout.addLayout(self.buttonLayout, 0, 1)

        self.lastSearch = ''
        self.numberOfScannedPages = 0
        self.searchButton = QtWidgets.QPushButton()
        self.searchButton.setText('Search')
        self.searchButton.setToolTip('Search for books using inputted query')
        self.searchButton.clicked.connect(self.searchBooks)
        self.buttonLayout.addWidget(self.searchButton)

        self.getMoreBooksPageCountInput = QtWidgets.QSpinBox()
        self.getMoreBooksPageCountInput.setMinimum(1)
        self.getMoreBooksPageCountInput.setValue(1)
        self.getMoreBooksPageCountInput.setSuffix(' pages')
        self.getMoreBooksPageCountInput.setToolTip('Number of pages to scan for more books (usually 25 books/page)')
        self.buttonLayout.addWidget(self.getMoreBooksPageCountInput)

        self.getMoreBooksButton = QtWidgets.QPushButton()
        self.getMoreBooksButton.setText('Get more books')
        self.getMoreBooksButton.setToolTip('Scan more pages for more books (usually 25 books/page)')
        self.getMoreBooksButton.clicked.connect(self.getMoreBooks)
        self.buttonLayout.addWidget(self.getMoreBooksButton)

        self.numberOfScannedPagesLabel = GenericWidgets.DefaultLabel()
        self.numberOfScannedPagesLabel.setStyleSheet(self.defaultStylesheet)
        self.numberOfScannedPagesLabel.setText(f'Scanned {str(self.numberOfScannedPages)} pages')
        self.numberOfScannedPagesLabel.setToolTip('Number of scanned pages for books')
        self.buttonLayout.addWidget(self.numberOfScannedPagesLabel)

        self.addToLibraryButton = QtWidgets.QPushButton()
        self.addToLibraryButton.setText('Add to library')
        self.addToLibraryButton.setToolTip('Add selected books to the library')
        self.addToLibraryButton.clicked.connect(self.addSelectedToLibrary)
        self.buttonLayout.addWidget(self.addToLibraryButton)


    def searchBooks(self):
        self.lastSearch = self.searchInput.text()
        self.moreBooksAvailable = True

        self.config = ConfigUtils.loadConfig()

        n = self.config['NUMBER_OF_PAGES_TO_SCAN']

        if n > 0:
            self.bookData = ScrapingUtils.search(self.lastSearch)

        self.numberOfScannedPages = 1
        self.numberOfScannedPagesLabel.setStyleSheet(self.defaultStylesheet)
        self.numberOfScannedPagesLabel.setText(f'Scanned {str(self.numberOfScannedPages)} pages')
        n -= 1

        rowWidgets = [ComicTableWidgetItemSet(entry) for entry in self.bookData]
        self.searchResultContainer.setRowCount(0)

        for rowWidget in rowWidgets:
            rowWidget.appendSelf(self.searchResultContainer)

        if n > 0:
            self.getMoreBooks(n)
    
    def getMoreBooks(self, n = None):
        numberOfPages = n or self.getMoreBooksPageCountInput.value()
        books = []

        for _ in range(numberOfPages):
            if self.moreBooksAvailable:
                _ = ScrapingUtils.search(self.lastSearch, self.numberOfScannedPages + 1)
                l = len(_)
                books.extend(_)
                if l < 25:
                    if l > 0:
                        self.numberOfScannedPages += 1
                    self.numberOfScannedPagesLabel.setText(f'Scanned {str(self.numberOfScannedPages)} pages')
                    self.moreBooksAvailable = False
                    self.numberOfScannedPagesLabel.setStyleSheet(self.highlightStylesheet)
                    break
                self.numberOfScannedPages += 1
                self.numberOfScannedPagesLabel.setText(f'Scanned {str(self.numberOfScannedPages)} pages')


        self.bookData.extend(books)

        rowWidgets = [ComicTableWidgetItemSet(entry) for entry in books]

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
