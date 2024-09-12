from PySide6 import QtWidgets, QtGui
from . import SettingsUtils
from . import GenericWidgets
from . import LocalUtils
from .QtUtils import *


class LocalWidget(QtWidgets.QWidget):
    def __init__(self, readingTarget):
        super().__init__()
        self.readingTarget = readingTarget
        

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
        self.searchCriteriaInput.addItem('Status')
        self.searchCriteriaInput.addItem('Release Year')
        self.searchCriteriaInput.addItem('Latest Issue')
        self.buttonLayout.addWidget(self.searchCriteriaInput)
        self.criteriaMap = {
            'Title': 'title',
            'Status': 'status',
            'Release Year': 'releaseYear',
            'Latest Issue': 'latest'
        }
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.setToolTip('Type here to search, press Enter to confirm')
        self.searchInput.returnPressed.connect(self.defaultSearch)
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
        self.refreshButton.clicked.connect(self.refresh)
        self.buttonLayout.addWidget(self.refreshButton)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setText('Delete books')
        self.deleteButton.setToolTip('Delete selected books from the library (including issues and reading progress)')
        self.deleteButton.clicked.connect(self.deleteSelected)
        self.buttonLayout.addWidget(self.deleteButton)

        
        self.refresh()

    def insertBook(self, data):
        rowCount = self.bookContainer.rowCount()

        background = QtGui.QBrush(self.settings['COLOR_ISSUE_ALREADY_DOWNLOADED'])
        self.bookContainer.setRowCount(rowCount + 1)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(background)
            self.bookContainer.setItem(rowCount, i, cell)
    
    def search(self, query, criteria):
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
            self.insertBook([info['title'], info['status'], info['releaseYear'], info['latest']])

    def defaultSearch(self):
        return self.search(self.searchInput.text(), self.criteriaMap[self.searchCriteriaInput.currentText()])

    def refresh(self):
        self.hidePreview()
        self.bookContainer.setRowCount(0)
        self.settings = SettingsUtils.loadSettings()
        self.books = [LocalUtils.getBookInfo(book) for book in LocalUtils.getBooks()]

        for cb in self.books:
            info = cb['info']
            self.insertBook([info['title']])

    def hidePreview(self):
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.issueLibrary = None

    def showPreview(self, name):
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.issueLibrary = IssueLocalWidget(name, self.readingTarget)
        self.gridLayout.addWidget(self.issueLibrary, 1, 1)

    def handleSelectionChanged(self):
        first = self.bookContainer.selectedIndexes()
        if len(first) > 0:
            self.showPreview(self.bookContainer.item(first[0].row(), 0).text())

    def deleteSelected(self):
        rows = set([i.row() for i in self.bookContainer.selectedIndexes()])
        bookDetails = [self.books[row] for row in rows]
        for book in bookDetails:
            LocalUtils.deleteBook(book['info']['title'])
            self.refresh()

class IssueLocalWidget(QtWidgets.QWidget):
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

        self.readButton = QtWidgets.QPushButton()
        self.readButton.setText('Read')
        self.readButton.setToolTip('Read selected issues')
        self.readButton.clicked.connect(self.readSelected)
        self.buttonLayout.addWidget(self.readButton)

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
        settings = SettingsUtils.loadSettings()
        brush = QtGui.QBrush(settings['COLOR_ISSUE_ALREADY_DOWNLOADED'])
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(brush)
            self.issueContainer.setItem(rowCount, i, cell)

    def refresh(self):
        self.downloadedIssues = LocalUtils.getIssues(self.title)
        self.details = LocalUtils.getBookInfo(self.title)
        self.details['info']['numberOfDownloadedIssues'] = len(self.downloadedIssues)
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
        data['size'] = LocalUtils.parseSize(LocalUtils.getBookSize(self.title))
        self.preview = GenericWidgets.ComicPreviewWidget(data, False)
        self.gridLayout.addWidget(self.preview, 1, 0)
        self.preview.show()


    def readSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        for issue in issuesDetails:
            issueName = issue['name']
            if issueName in self.downloadedIssues:
                self.readingTarget.addReaderTab(self.title, issueName)

    def deleteSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]
        for issue in issuesDetails:
            LocalUtils.deleteIssue(self.title, issue['name'])
        self.refresh()
