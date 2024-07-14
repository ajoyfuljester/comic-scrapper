from PySide6 import QtWidgets, QtGui

from GenericWidgets import ResizingLabel
import LibraryUtils



class ReaderWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

    def addReaderTab(self, comicBookName, issueName):
        self.addTab(ReaderTab(comicBookName, issueName), issueName)

class ReaderTab(QtWidgets.QWidget):
    def __init__(self, comicBookName, issueName):
        super().__init__()

        self.comicBookName = comicBookName
        self.issueName = issueName

        self.gridLayout = QtWidgets.QGridLayout(self)
        
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(self.buttonLayout, 0, 1)

        self.nextPageButton = QtWidgets.QPushButton()
        self.nextPageButton.setText('Next page')
        self.nextPageButton.clicked.connect(self.nextPage)
        self.buttonLayout.addWidget(self.nextPageButton)

        self.previousPageButton = QtWidgets.QPushButton()
        self.previousPageButton.setText('Previous page')
        self.previousPageButton.clicked.connect(self.previousPage)
        self.buttonLayout.addWidget(self.previousPageButton)

        self.pages = LibraryUtils.getIssuePages(comicBookName, issueName)
        self.numberOfPages = len(self.pages)

        self.currentPageNumber = 0
        self.setPage(self.currentPageNumber)

    def setPage(self, number):
        if number >= self.numberOfPages or number < 0:
            return
        last = self.gridLayout.itemAtPosition(0, 0)
        if last:
            last.widget().deleteLater()
        pixmap = QtGui.QPixmap()
        pixmap.load(self.pages[number])
        self.currentPageNumber = number
        self.currentPage = ResizingLabel(pixmap)
        self.gridLayout.addWidget(self.currentPage, 0, 0)

    def nextPage(self):
        self.setPage(self.currentPageNumber + 1)

    def previousPage(self):
        self.setPage(self.currentPageNumber - 1)
