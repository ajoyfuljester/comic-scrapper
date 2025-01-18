from PySide6 import QtWidgets, QtGui
from . import LibraryUtils
from . import ScrapingUtils
from .QtUtils import *
from .GenericWidgets import ComicPreviewWidget
from . import SettingsUtils
from Stuff import GenericWidgets

class BrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settings = SettingsUtils.loadSettings()
        self.highlightStylesheet = f"color: {self.settings['COLOR_ACCENT']};"
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.setToolTip('Type here to search, press Enter to confirm')
        self.searchInput.returnPressed.connect(self.searchBooks)

        self.searchResultContainer = QtWidgets.QTableWidget()
        self.searchResultContainer.setColumnCount(1)
        self.searchResultContainer.setHorizontalHeaderLabels(['Title'])
        tableHeader = self.searchResultContainer.horizontalHeader()
        tableHeader.setSectionResizeMode(0, ResizeMode.Stretch)
#         tableHeader.setSectionResizeMode(1, ResizeMode.ResizeToContents)
#         tableHeader.setSectionResizeMode(2, ResizeMode.ResizeToContents)
#         tableHeader.setSectionResizeMode(3, ResizeMode.Stretch)


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
        self.numberOfScrapedPages = 0
        self.searchButton = QtWidgets.QPushButton()
        self.searchButton.setText('Search')
        self.searchButton.setToolTip('Search for books using inputted query')
        self.searchButton.clicked.connect(self.searchBooks)
        self.buttonLayout.addWidget(self.searchButton)

        self.getMoreBooksPageCountInput = QtWidgets.QSpinBox()
        self.getMoreBooksPageCountInput.setDisabled(True)
        self.getMoreBooksPageCountInput.setMinimum(1)
        self.getMoreBooksPageCountInput.setValue(1)
        self.getMoreBooksPageCountInput.setSuffix(' pages')
        self.getMoreBooksPageCountInput.setToolTip('Number of pages to scrape for more books (usually 25 books/page)\n[UNAVAILABLE]')
        self.buttonLayout.addWidget(self.getMoreBooksPageCountInput)

        self.getMoreBooksButton = QtWidgets.QPushButton()
        self.getMoreBooksButton.setDisabled(True)
        self.getMoreBooksButton.setText('Get more books')
        self.getMoreBooksButton.setToolTip('Scrape more pages for more books (usually 25 books/page)\n[UNAVAILABLE]')
        self.getMoreBooksButton.clicked.connect(self.getMoreBooks)
        self.buttonLayout.addWidget(self.getMoreBooksButton)

        self.numberOfScrapedPagesLabel = GenericWidgets.DefaultLabel()
        self.numberOfScrapedPagesLabel.setText(f'Scraped {str(self.numberOfScrapedPages)} pages')
        self.numberOfScrapedPagesLabel.setToolTip('Number of scraped pages for books (if highlighted then no more pages)')
        self.buttonLayout.addWidget(self.numberOfScrapedPagesLabel)

        self.addToLibraryButton = QtWidgets.QPushButton()
        self.addToLibraryButton.setText('Add to library')
        self.addToLibraryButton.setToolTip('Add selected books to the library')
        self.addToLibraryButton.clicked.connect(self.addSelectedToLibrary)
        self.buttonLayout.addWidget(self.addToLibraryButton)


    def searchBooks(self):
        self.lastSearch = self.searchInput.text()
        self.moreBooksAvailable = True

        self.settings = SettingsUtils.loadSettings()

        n = self.settings['NUMBER_OF_PAGES_TO_SCRAPE']

        if n > 0:
            if self.settings["USE_LIST"]:
                self.bookData = LibraryUtils.searchList(self.lastSearch, self.settings["LIST_MAX_MATCHES"])
            else:
                self.bookData = ScrapingUtils.search(self.lastSearch)

        self.numberOfScrapedPages = 1
        self.numberOfScrapedPagesLabel.setStyleSheet('')
        self.numberOfScrapedPagesLabel.setText(f'Scraped {str(self.numberOfScrapedPages)} pages')
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
                _ = ScrapingUtils.search(self.lastSearch, self.numberOfScrapedPages + 1)
                l = len(_)
                books.extend(_)
                if l < 25:
                    if l > 0:
                        self.numberOfScrapedPages += 1
                    self.numberOfScrapedPagesLabel.setText(f'Scraped {str(self.numberOfScrapedPages)} pages')
                    self.moreBooksAvailable = False
                    self.numberOfScrapedPagesLabel.setStyleSheet(self.highlightStylesheet)
                    break
                self.numberOfScrapedPages += 1
                self.numberOfScrapedPagesLabel.setText(f'Scraped {str(self.numberOfScrapedPages)} pages')


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

        
        if self.settings["USE_LIST"]:
            l = LibraryUtils.loadList()
            for cb in selectedComicBooks:
                LibraryUtils.addToLibrary(cb['URL'], l['selector'], l['innerSelector'], l['urlSuffix'])
        else:
            for cb in selectedComicBooks:
                LibraryUtils.addToLibrary(cb['URL'])
        

        
class ComicTableWidgetItemSet():
    def __init__(self, details):
        self.settings = SettingsUtils.loadSettings()
        self.highlightBackground = self.settings['COLOR_BOOK_ALREADY_IN_LIBRARY']

        self.cellData = [
            details['title'],
        ]


        self.cellWidgets = [QtWidgets.QTableWidgetItem(cell) for cell in self.cellData]
        highlight = LibraryUtils.forceFilename(self.cellData[0]) in LibraryUtils.getBooks()
        brush = QtGui.QBrush(self.highlightBackground if highlight else self.settings['COLOR_CELL'])
        for cell in self.cellWidgets:
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(brush)

    
    def appendSelf(self, target):
        lastRow = target.rowCount()
        target.setRowCount(lastRow + 1)
        for i, cell in enumerate(self.cellWidgets):
            target.setItem(lastRow, i, cell)
