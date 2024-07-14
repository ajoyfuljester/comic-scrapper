from PySide6 import QtWidgets, QtGui
import ConfigUtils
import GenericWidgets
import LibraryUtils
from QtUtils import *
from ReaderWidget import ReaderWidget


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self, readingTarget):
        super().__init__()
        self.readingTarget = readingTarget
        
        LibraryUtils.createLibraryIfDoesNotExist()


        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)

        self.searchCriteriaInput = QtWidgets.QComboBox()
        self.searchCriteriaInput.addItem('Title')
        self.searchCriteriaInput.addItem('Status')
        self.searchCriteriaInput.addItem('Release Year')
        self.searchCriteriaInput.addItem('Latest Issue')
        self.gridLayout.addWidget(self.searchCriteriaInput, 0, 1)
        criteriaMap = {
            'Title': 'title',
            'Status': 'status',
            'Release Year': 'releaseYear',
            'Latest Issue': 'latest'
        }
        
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText('Type here to search')
        self.searchInput.returnPressed.connect(lambda: self.searchComicBooks(self.searchInput.text(), criteriaMap[self.searchCriteriaInput.currentText()]))
        self.gridLayout.addWidget(self.searchInput, 0, 0)

        self.comicBookContainer = QtWidgets.QTableWidget()
        self.comicBookContainer.setColumnCount(4)
        self.comicBookContainer.setHorizontalHeaderLabels(['Title', 'Status', 'Release Year', 'Latest Issue'])
        tableHeaders = self.comicBookContainer.horizontalHeader()
        tableHeaders.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(2, ResizeMode.ResizeToContents)
        tableHeaders.setSectionResizeMode(3, ResizeMode.Stretch)
        self.comicBookContainer.itemSelectionChanged.connect(self.handleSelectionChanged)
        self.gridLayout.addWidget(self.comicBookContainer, 1, 0)

        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setText('Refresh List')
        self.refreshButton.clicked.connect(self.refreshComicBooks)

        self.gridLayout.addWidget(self.refreshButton, 0, 2)
        
        self.refreshComicBooks()

    def insertComicBook(self, data):
        rowCount = self.comicBookContainer.rowCount()

        self.comicBookContainer.setRowCount(rowCount + 1)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            self.comicBookContainer.setItem(rowCount, i, cell)
    
    def searchComicBooks(self, query, criteria): # maybe this function should be in LibraryUtils
        self.comicBookContainer.setRowCount(0)
        l = len(query)
        sortedComicBooks = [[-1, cb] for cb in self.comicBooks]
        for i in range(1, l + 1):
            for cb in sortedComicBooks:
                found = cb[1]['info'][criteria].find(query[:i])
                if found != -1:
                    cb[0] = i

        sortedComicBooks.sort(key=lambda x: x[0], reverse=True)

        for _, cb in sortedComicBooks:
            info = cb['info']
            self.insertComicBook([info['title'], info['status'], info['releaseYear'], info['latest']])


    def refreshComicBooks(self):
        self.comicBookContainer.setRowCount(0)
        self.comicBooks = [LibraryUtils.getComicBookInfo(cb) for cb in LibraryUtils.getComicBooks()]

        for cb in self.comicBooks:
            info = cb['info']
            self.insertComicBook([info['title'], info['status'], info['releaseYear'], info['latest']])

    def showPreview(self, name):
        last = self.gridLayout.itemAtPosition(1, 1)
        if last:
            last.widget().deleteLater()
        self.issueLibrary = IssueLibraryWidget(name, self.readingTarget)
        self.gridLayout.addWidget(self.issueLibrary, 1, 1, 1, 2)

    def handleSelectionChanged(self):
        first = self.comicBookContainer.selectedIndexes()
        if len(first) > 0:
            self.showPreview(self.comicBookContainer.item(first[0].row(), 0).text())

class IssueLibraryWidget(QtWidgets.QWidget):
    defaultBackground = 'white'
    def __init__(self, name, readingTarget):
        super().__init__()
        self.comicBookName = name
        self.readingTarget = readingTarget or self.parentWidget()

        self.highlightBackground = ConfigUtils.loadConfig()['COLOR_ISSUE_ALREADY_DOWNLOADED']

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


        self.downloadedIssues = LibraryUtils.getDownloadedComicBookIssues(self.comicBookName)
        self.details = LibraryUtils.getComicBookInfo(name)
        self.details['info']['numberOfDownloadedIssues'] = len(self.downloadedIssues)
        self.preview = GenericWidgets.ComicPreviewWidget(self.details['info'], False)
        self.gridLayout.addWidget(self.preview, 1, 0, 1, 2)

        self.buttonLayout = QtWidgets.QVBoxLayout()

        self.downloadButton = QtWidgets.QPushButton()
        self.downloadButton.setText('Download')
        self.downloadButton.clicked.connect(self.downloadSelected)
        self.buttonLayout.addWidget(self.downloadButton)

        self.readButton = QtWidgets.QPushButton()
        self.readButton.setText('Read')
        self.readButton.clicked.connect(self.readSelected)
        self.buttonLayout.addWidget(self.readButton)

        self.gridLayout.addLayout(self.buttonLayout, 0, 1)

        self.refreshIssues()

    def insertIssue(self, data):
        rowCount = self.issueContainer.rowCount()
        data = list(data)

        self.issueContainer.setRowCount(rowCount + 1)
        highlight = data[0] in self.downloadedIssues
        brush = QtGui.QBrush(self.highlightBackground if highlight else self.defaultBackground)
        for i, value in enumerate(data):
            cell = QtWidgets.QTableWidgetItem(value)
            cell.setFlags(ItemFlag.ItemIsSelectable | ItemFlag.ItemIsEnabled)
            cell.setBackground(brush)
            self.issueContainer.setItem(rowCount, i, cell)

    def refreshIssues(self):
        self.downloadedIssues = LibraryUtils.getDownloadedComicBookIssues(self.comicBookName)
        config = ConfigUtils.loadConfig()
        self.issueContainer.setRowCount(0)
        issues = self.details['issues']
        
        if config['INVERT_ISSUE_ORDER']:
            issues.reverse()
        for issue in issues:
            self.insertIssue(issue.values())

    def downloadSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        for issue in issuesDetails:
            LibraryUtils.downloadIssue(self.comicBookName, issue)

        self.refreshIssues()


    def readSelected(self):
        rows = set([i.row() for i in self.issueContainer.selectedIndexes()])
        issuesDetails = [self.details['issues'][row] for row in rows]

        for issue in issuesDetails:
            issueName = issue['name']
            if issueName in self.downloadedIssues:
                self.readingTarget.addReaderTab(self.comicBookName, issueName)
