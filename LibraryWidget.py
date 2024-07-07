from PySide6 import QtWidgets
import LibraryUtils
from QtUtils import *


class LibraryWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        LibraryUtils.createLibraryIfDoesNotExist()


        self.gridLayout = QtWidgets.QGridLayout(self)

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
        self.comicBooks = [LibraryUtils.comicBookInfo(cb) for cb in LibraryUtils.comicBooks()]

        for cb in self.comicBooks:
            info = cb['info']
            self.insertComicBook([info['title'], info['status'], info['releaseYear'], info['latest']])
