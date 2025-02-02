from PySide6 import QtWidgets, QtGui
from . import SettingsUtils
from . import GenericWidgets
from . import LibraryUtils
from .QtUtils import *


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self, readingTarget):
        super().__init__()
        self.readingTarget = readingTarget
        
        LibraryUtils.createLibraryIfDoesNotExist()


        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.gridLayout.addLayout(self.buttonLayout, 0, 1)

        self.searchButton = QtWidgets.QPushButton()
        self.searchButton.setText('Search')
        self.searchButton.setToolTip('Search for books using inputted query')
        self.searchButton.clicked.connect(self.defaultSearch)
        self.buttonLayout.addWidget(self.searchButton)

        self.searchCriteriaInput = QtWidgets.QComboBox()
        self.searchCriteriaInput.addItem('Title')
#         self.searchCriteriaInput.addItem('Status')
#         self.searchCriteriaInput.addItem('Release Year')
#         self.searchCriteriaInput.addItem('Latest Issue')
        self.buttonLayout.addWidget(self.searchCriteriaInput)
        self.criteriaMap = {
            'Title': 'title',
#             'Status': 'status',
            'Release Year': 'releaseYear',
            'Latest Issue': 'latest'
        }
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.setToolTip('Type here to search, press Enter to confirm')
        self.searchInput.returnPressed.connect(self.defaultSearch)
        self.gridLayout.addWidget(self.searchInput, 0, 0)

        self.bookContainer = QtWidgets.QTableWidget()
        self.bookContainer.setColumnCount(len(self.criteriaMap))
        self.bookContainer.setHorizontalHeaderLabels(self.criteriaMap.keys())
        tableHeaders = self.bookContainer.horizontalHeader()
        tableHeaders.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(2, ResizeMode.Stretch)
#         tableHeaders.setSectionResizeMode(3, ResizeMode.Stretch)
        self.bookContainer.itemSelectionChanged.connect(self.handleSelectionChanged)
        self.gridLayout.addWidget(self.bookContainer, 1, 0)

        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setText('Refresh books')
        self.refreshButton.setToolTip('Refresh books in the library')
        self.refreshButton.clicked.connect(self.refresh)
        self.buttonLayout.addWidget(self.refreshButton)

        self.updateButton = QtWidgets.QPushButton()
        self.updateButton.setText('Update books')
        self.updateButton.setToolTip('Update selected books in the library - pull data from the website')
        self.updateButton.clicked.connect(self.updateSelected)
        self.buttonLayout.addWidget(self.updateButton)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setText('Delete books')
        self.deleteButton.setToolTip('Delete selected books from the library (including issues and reading progress)')
        self.deleteButton.clicked.connect(self.deleteSelected)
        self.buttonLayout.addWidget(self.deleteButton)

        
        self.refresh()

    def insertBook(self, data):
        rowCount = self.bookContainer.rowCount()

        readingProgress = LibraryUtils.getReadingProgress(data[0])
        isRead = all(issue['isRead'] for issue in readingProgress)
        isDownloaded = sorted([LibraryUtils.forceFilename(issue['name']) for issue in readingProgress]) == sorted(LibraryUtils.getDownloadedIssues(data[0]))

        background = QtGui.QBrush(self.settings['COLOR_CELL'])
        if isRead:
            background = QtGui.QBrush(self.settings['COLOR_ISSUE_ALREADY_READ'])
        if isDownloaded:
            background = QtGui.QBrush(self.settings['COLOR_ISSUE_ALREADY_DOWNLOADED'])
        if isRead and isDownloaded:
            background = QtGui.QBrush(self.settings['COLOR_ISSUE_ALREADY_DOWNLOADED_AND_READ'])
        self.bookContainer.setRowCount(rowCount + 1)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(background)
            self.bookContainer.setItem(rowCount, i, cell)
    
    def search(self, query, criteria): # maybe this function should be in LibraryUtils
        self.bookContainer.setRowCount(0)
        l = len(query)
        sortedComicBooks = [[-1, cb] for cb in self.books]
        for i in range(1, l + 1):
            for cb in sortedComicBooks:
                found = cb[1]['info'][criteria].find(query[:i])
                if found != -1:
                    cb[0] = i

        sortedComicBooks.sort(key=lambda x: x[0], reverse=True)

        for _, cb in sortedComicBooks:
            info = cb['info']
            self.insertBook([info['title'], info['releaseYear'], info['latest']])

    def defaultSearch(self):
        return self.search(self.searchInput.text(), self.criteriaMap[self.searchCriteriaInput.currentText()])

    def refresh(self):
        self.hidePreview()
        self.bookContainer.setRowCount(0)
        self.settings = SettingsUtils.loadSettings()
        self.books = [LibraryUtils.getBookInfo(book) for book in LibraryUtils.getBooks()]

        for cb in self.books:
            info = cb['info']
            self.insertBook([info['title'], info['releaseYear'], info['latest']])

    def hidePreview(self):
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.issueLibrary = None

    def showPreview(self, name):
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.issueLibrary = IssueLibraryWidget(name, self.readingTarget)
        self.gridLayout.addWidget(self.issueLibrary, 1, 1)

    def handleSelectionChanged(self):
        first = self.bookContainer.selectedIndexes()
        if len(first) > 0:
            self.showPreview(self.bookContainer.item(first[0].row(), 0).text())

    def deleteSelected(self):
        rows = set([i.row() for i in self.bookContainer.selectedIndexes()])
        bookDetails = [self.books[row] for row in rows]
        for book in bookDetails:
            LibraryUtils.deleteBook(book['info']['title'])
            self.refresh()

    def updateSelected(self):
        rows = set([i.row() for i in self.bookContainer.selectedIndexes()])
        bookDetails = [self.books[row] for row in rows]
        for book in bookDetails:
            LibraryUtils.updateBook(book['info']['URL'])
            self.refresh()

class IssueLibraryWidget(QtWidgets.QWidget):
    needsRefresh = QtCore.Signal()

    def __init__(self, title, readingTarget):
        super().__init__()
        self.title = title
        self.readingTarget = readingTarget or self.parentWidget()

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)


        self.issueContainer = QtWidgets.QTableWidget()
        self.issueContainer.setColumnCount(2)
        self.issueContainer.setHorizontalHeaderLabels(['Title', 'URL'])
        tableHeaders = self.issueContainer.horizontalHeader()
        tableHeaders.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(1, ResizeMode.Stretch)
        self.gridLayout.addWidget(self.issueContainer, 0, 0)


        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.downloadButton = QtWidgets.QPushButton()
        self.downloadButton.setText('Download')
        self.downloadButton.setToolTip('Download selected issues')
        self.downloadButton.clicked.connect(self.downloadSelected)
        self.buttonLayout.addWidget(self.downloadButton)

        self.readButton = QtWidgets.QPushButton()
        self.readButton.setText('Read')
        self.readButton.setToolTip('Read selected issues')
        self.readButton.clicked.connect(self.readSelected)
        self.buttonLayout.addWidget(self.readButton)

        self.markAsReadButton = QtWidgets.QPushButton()
        self.markAsReadButton.setText('Mark as read')
        self.markAsReadButton.setToolTip('Mark selected issues as read')
        self.markAsReadButton.clicked.connect(lambda: self.markSelected(True))
        self.buttonLayout.addWidget(self.markAsReadButton)

        self.markAsUnreadButton = QtWidgets.QPushButton()
        self.markAsUnreadButton.setText('Mark as unread')
        self.markAsUnreadButton.setToolTip('Mark selected issues as unread')
        self.markAsUnreadButton.clicked.connect(lambda: self.markSelected(False))
        self.buttonLayout.addWidget(self.markAsUnreadButton)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setText('Delete issues')
        self.deleteButton.setToolTip('Delete selected issues (does not mark issues as unread)')
        self.deleteButton.clicked.connect(self.deleteSelected)
        self.buttonLayout.addWidget(self.deleteButton)

        self.gridLayout.addLayout(self.buttonLayout, 2, 0)

        self.needsRefresh.connect(self.refresh)


        self.refresh()

    def insertIssue(self, data):
        rowCount = self.issueContainer.rowCount()
        data = list(data)

        self.issueContainer.setRowCount(rowCount + 1)
        isDownloaded = LibraryUtils.forceFilename(data[0]) in self.downloadedIssues
        index = [p['name'] for p in self.readingProgress].index(data[0])
        isRead = self.readingProgress[index]['isRead']
        settings = SettingsUtils.loadSettings()
        self.highlightDownloadedBackground = settings['COLOR_ISSUE_ALREADY_DOWNLOADED']
        self.highlightReadBackground = settings['COLOR_ISSUE_ALREADY_READ']
        self.highlightDownloadedAndReadBackground = settings['COLOR_ISSUE_ALREADY_DOWNLOADED_AND_READ']
        brush = QtGui.QBrush(self.settings['COLOR_CELL'])
        if isDownloaded:
            brush = QtGui.QBrush(self.highlightDownloadedBackground)
        if isRead:
            brush = QtGui.QBrush(self.highlightReadBackground)
        if isDownloaded and isRead:
            brush = QtGui.QBrush(self.highlightDownloadedAndReadBackground)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(brush)
            self.issueContainer.setItem(rowCount, i, cell)

    def refresh(self):
        self.downloadedIssues = LibraryUtils.getDownloadedIssues(self.title)
        self.readingProgress = LibraryUtils.getReadingProgress(self.title)
        self.details = LibraryUtils.getBookInfo(self.title)
        self.details['info']['numberOfDownloadedIssues'] = len(self.downloadedIssues)
        self.details['info']['numberOfReadIssues'] = len(list(filter(lambda p: p['isRead'], self.readingProgress)))
        self.settings = SettingsUtils.loadSettings()
        self.issueContainer.setRowCount(0)
        issues = self.details['issues']
        
        if self.settings['INVERT_ISSUE_ORDER']:
            issues.reverse()
        for issue in issues:
            self.insertIssue(issue.values())

        lastPreview = self.gridLayout.itemAtPosition(1, 0)
        if lastPreview:
            lastPreview.widget().deleteLater()

        data = self.details['info']
        data['size'] = LibraryUtils.parseSize(LibraryUtils.getBookSize(self.title))
        self.preview = GenericWidgets.ComicPreviewWidget(data, False)
        self.gridLayout.addWidget(self.preview, 1, 0)
        self.preview.show()

    def downloadSelected(self):
        self.settings = SettingsUtils.loadSettings()
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        columnCount = self.issueContainer.columnCount()
        highlightBackground = QtGui.QBrush(self.settings['COLOR_ISSUE_DOWNLOAD_PENDING'])
        for y in rows:
            for x in range(columnCount):
                self.issueContainer.item(y, x).setBackground(highlightBackground)
        for issue in issuesDetails:
            innerSelector = self.details['info'].get('innerSelector', None)
            LibraryUtils.downloadIssueAsThread(self.title, issue, innerSelector, None, self.needsRefresh.emit)


    def readSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        for issue in issuesDetails:
            issueName = issue['name']
            if LibraryUtils.forceFilename(issueName) in self.downloadedIssues:
                self.readingTarget.addReaderTab(self.title, issueName)

    def markSelected(self, isRead = True):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]
        for issue in issuesDetails:
            LibraryUtils.markIssueReadingProgress(self.title, issue['name'], isRead)
        self.refresh()

    def deleteSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]
        for issue in issuesDetails:
            LibraryUtils.deleteIssue(self.title, issue['name'])
        self.refresh()
