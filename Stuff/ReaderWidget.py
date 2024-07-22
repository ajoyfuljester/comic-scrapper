from PySide6 import QtWidgets, QtGui
from . import ConfigUtils
from .GenericWidgets import ResizingLabel, DefaultLabel
from . import LibraryUtils
from .QtUtils import *



class ReaderWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

        self.tabCloseRequested.connect(self.removeTab)

    def addReaderTab(self, title, issue, page = 0):
        tab = ReaderTab(title, issue)
        tab.setPage(page)
        self.addTab(tab, issue)

class ReaderTab(QtWidgets.QWidget):
    bigFont = QtGui.QFont()
    bigFont.setPixelSize(12 * 2)
    def __init__(self, title, issue):
        super().__init__()

        self.title = title
        self.issue = issue

        self.gridLayout = QtWidgets.QGridLayout(self)
        
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.gridLayout.addLayout(self.bottomLayout, 1, 0)

        self.previousPageButton = QtWidgets.QPushButton()
        self.previousPageButton.setText('Previous page')
        self.previousPageButton.clicked.connect(self.previousPage)
        self.previousPageButton.setShortcut(Key.Key_Left)
        self.bottomLayout.addWidget(self.previousPageButton, 1)


        self.pages = LibraryUtils.getIssuePagesPaths(self.title, self.issue)
        self.numberOfPages = len(self.pages)

        self.pageNumberInput = QtWidgets.QLineEdit()
        self.pageNumberInput.setPlaceholderText('Page number')
        self.pageNumberInput.textEdited.connect(self.handlePageNumberInput)
        self.numberOfPagesLabel = DefaultLabel()
        self.numberOfPagesLabel.setText('/' + str(self.numberOfPages))
        self.bottomLayout.addWidget(self.pageNumberInput, 0)
        self.bottomLayout.addWidget(self.numberOfPagesLabel, 0)

        self.nextPageButton = QtWidgets.QPushButton()
        self.nextPageButton.setText('Next page')
        self.nextPageButton.clicked.connect(self.nextPage)
        self.nextPageButton.setShortcut(Key.Key_Right)
        self.bottomLayout.addWidget(self.nextPageButton, 1)

        self.currentPageNumber = 0
        self.setPage(self.currentPageNumber)

    def setPage(self, number):
        config = ConfigUtils.loadConfig()
        if number >= self.numberOfPages or number < 0:
            return self.currentPageNumber
        last = self.gridLayout.itemAtPosition(0, 0)
        if last:
            last.widget().deleteLater()
        pixmap = QtGui.QPixmap()
        pixmap.load(self.pages[number])
        self.currentPageNumber = number
        self.currentPage = ResizingLabel(pixmap)
        self.currentPage.setAlignment(Alignment.AlignCenter)
        self.gridLayout.addWidget(self.currentPage, 0, 0)
        self.pageNumberInput.setText(str(number + 1))

        if config['MARK_AS_AFTER_LAST_PAGE'] and self.currentPageNumber == self.numberOfPages - 1:
            LibraryUtils.markIssueReadingProgress(self.title, self.issue)

        return self.currentPageNumber

    def nextPage(self):
        self.setPage(self.currentPageNumber + 1)

    def previousPage(self):
        self.setPage(self.currentPageNumber - 1)

    def handlePageNumberInput(self, text):
        try:
            i = int(text) - 1
            return self.setPage(i)
        except ValueError:
            pass

