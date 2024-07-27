from PySide6 import QtWidgets, QtGui
from . import ConfigUtils
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

        self.searchCriteriaInput = QtWidgets.QComboBox()
        self.searchCriteriaInput.addItem('Title')
        self.searchCriteriaInput.addItem('Status')
        self.searchCriteriaInput.addItem('Release Year')
        self.searchCriteriaInput.addItem('Latest Issue')
        self.buttonLayout.addWidget(self.searchCriteriaInput)
        criteriaMap = {
            'Title': 'title',
            'Status': 'status',
            'Release Year': 'releaseYear',
            'Latest Issue': 'latest'
        }
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.setToolTip('Type here to search, press Enter to confirm')
        self.searchInput.returnPressed.connect(lambda: self.searchComicBooks(self.searchInput.text(), criteriaMap[self.searchCriteriaInput.currentText()]))
        self.gridLayout.addWidget(self.searchInput, 0, 0)

        self.bookContainer = QtWidgets.QTableWidget()
        self.bookContainer.setColumnCount(4)
        self.bookContainer.setHorizontalHeaderLabels(['Title', 'Status', 'Release Year', 'Latest Issue'])
        tableHeaders = self.bookContainer.horizontalHeader()
        tableHeaders.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(2, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(3, ResizeMode.Stretch)
        self.bookContainer.itemSelectionChanged.connect(self.handleSelectionChanged)
        self.gridLayout.addWidget(self.bookContainer, 1, 0)

        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setText('Refresh books')
        self.refreshButton.setToolTip('Refresh books in the library')
        self.refreshButton.clicked.connect(self.refreshBooks)
        self.buttonLayout.addWidget(self.refreshButton)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setText('Delete books')
        self.deleteButton.setToolTip('Delete selected books from the library (including issues and reading progress)')
        self.deleteButton.clicked.connect(self.deleteSelected)
        self.buttonLayout.addWidget(self.deleteButton)
        
        self.refreshBooks()

    def insertComicBook(self, data):
        rowCount = self.bookContainer.rowCount()

        self.bookContainer.setRowCount(rowCount + 1)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            self.bookContainer.setItem(rowCount, i, cell)
    
    def searchComicBooks(self, query, criteria): # maybe this function should be in LibraryUtils
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
            self.insertComicBook([info['title'], info['status'], info['releaseYear'], info['latest']])


    def refreshBooks(self):
        self.hidePreview()
        self.bookContainer.setRowCount(0)
        self.books = [LibraryUtils.getBookInfo(book) for book in LibraryUtils.getBooks()]

        for cb in self.books:
            info = cb['info']
            self.insertComicBook([info['title'], info['status'], info['releaseYear'], info['latest']])

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
            self.refreshBooks()

class IssueLibraryWidget(QtWidgets.QWidget):
    defaultBackground = 'white'

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
        self.deleteButton.setText('Delete')
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
        config = ConfigUtils.loadConfig()
        self.highlightDownloadedBackground = config['COLOR_ISSUE_ALREADY_DOWNLOADED']
        self.highlightReadBackground = config['COLOR_ISSUE_ALREADY_READ']
        self.highlightDownloadedAndReadBackground = config['COLOR_ISSUE_ALREADY_DOWNLOADED_AND_READ']
        brush = QtGui.QBrush(self.defaultBackground)
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
        self.downloadedIssues = LibraryUtils.getDownloadedComicBookIssues(self.title)
        self.readingProgress = LibraryUtils.getReadingProgress(self.title)
        self.details = LibraryUtils.getBookInfo(self.title)
        self.details['info']['numberOfDownloadedIssues'] = len(self.downloadedIssues)
        self.details['info']['numberOfReadIssues'] = len(list(filter(lambda p: p['isRead'], self.readingProgress)))
        config = ConfigUtils.loadConfig()
        self.issueContainer.setRowCount(0)
        issues = self.details['issues']
        
        if config['INVERT_ISSUE_ORDER']:
            issues.reverse()
        for issue in issues:
            self.insertIssue(issue.values())

        lastPreview = self.gridLayout.itemAtPosition(1, 0)
        if lastPreview:
            lastPreview.widget().deleteLater()
        self.preview = GenericWidgets.ComicPreviewWidget(self.details['info'], False)
        self.gridLayout.addWidget(self.preview, 1, 0)
        self.preview.show()

    def downloadSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        for issue in issuesDetails:
            LibraryUtils.downloadIssueAsThread(self.title, issue, None, self.needsRefresh.emit)


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
