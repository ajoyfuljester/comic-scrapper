from PySide6 import QtWidgets

from Stuff import LocalUtils
from .GenericWidgets import DefaultLabel
from .QtUtils import *
from . import LibraryUtils


class RawWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.gridLayout = QtWidgets.QGridLayout(self)


        self.addToLibraryWidget = QtWidgets.QGroupBox()
        self.gridLayout.addWidget(self.addToLibraryWidget, 1, 1)
        self.addToLibraryWidget.setTitle('Add to Library')

        self.addToLibraryLayout = QtWidgets.QFormLayout(self.addToLibraryWidget)
        
        self.addToLibraryURL = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(0, ItemRole.SpanningRole, self.addToLibraryURL)
        self.addToLibraryURL.setPlaceholderText('URL of the site with the issues')
        self.addToLibraryURL.setToolTip('For example https://azcomix.me/comic/the-sandman-1989')
        
        self.addToLibraryURLSuffix = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(1, ItemRole.SpanningRole, self.addToLibraryURLSuffix)
        self.addToLibraryURLSuffix.setPlaceholderText('URL suffix to add to each issue to make sure every image is on one page')
        self.addToLibraryURLSuffix.setToolTip('For example /full')
        
        self.addToLibrarySelector = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(2, ItemRole.SpanningRole, self.addToLibrarySelector)
        self.addToLibrarySelector.setPlaceholderText('CSS selector that grabs the issues that have `href` attribute')
        self.addToLibrarySelector.setToolTip('If you do not know how to get this, you should check out the Help tab')
        
        self.addToLibraryInnerSelector = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(3, ItemRole.SpanningRole, self.addToLibraryInnerSelector)
        self.addToLibraryInnerSelector.setPlaceholderText('CSS selector that grabs the images with `src` attribute in each issue')
        self.addToLibraryInnerSelector.setToolTip('If you do not know how to get this, you should check out the Help tab')

        self.addToLibraryConfirm = QtWidgets.QPushButton()
        self.addToLibraryLayout.setWidget(4, ItemRole.SpanningRole, self.addToLibraryConfirm)
        self.addToLibraryConfirm.setText('Attempt to add to Library')
        self.addToLibraryConfirm.setToolTip('i hope the program will not crash if you typed something wrong')
        self.addToLibraryConfirm.clicked.connect(self.addToLibrary)
        
        self.addToLibraryOutputLabel = DefaultLabel('Output:')
        self.addToLibraryLayout.setWidget(5, ItemRole.LabelRole, self.addToLibraryOutputLabel)
        self.addToLibraryOutputLabel.setToolTip('Output of the performed action')
        
        self.addToLibraryOutput = DefaultLabel()
        self.addToLibraryLayout.setWidget(5, ItemRole.FieldRole, self.addToLibraryOutput)
        self.addToLibraryOutput.setToolTip('Output of the performed action')


        self.directDownloadWidget = QtWidgets.QGroupBox()
        self.gridLayout.addWidget(self.directDownloadWidget, 1, 2)
        self.directDownloadWidget.setTitle('Direct download')

        self.directDownloadLayout = QtWidgets.QFormLayout(self.directDownloadWidget)
        
        self.directDownloadURL = QtWidgets.QLineEdit()
        self.directDownloadLayout.setWidget(0, ItemRole.SpanningRole, self.directDownloadURL)
        self.directDownloadURL.setPlaceholderText('URL of the site with the images')
        self.directDownloadURL.setToolTip('For example https://azcomix.me/the-little-endless-storybook/issue-full/full')
        
        self.directDownloadInnerSelector = QtWidgets.QLineEdit()
        self.directDownloadLayout.setWidget(1, ItemRole.SpanningRole, self.directDownloadInnerSelector)
        self.directDownloadInnerSelector.setPlaceholderText('CSS selector that grabs the images with `src` attribute in each issue')
        self.directDownloadInnerSelector.setToolTip('If you do not know how to get this, you should check out the Help tab')

        self.directDownloadConfirm = QtWidgets.QPushButton()
        self.directDownloadLayout.setWidget(2, ItemRole.SpanningRole, self.directDownloadConfirm)
        self.directDownloadConfirm.setText('Attempt to download the issue')
        self.directDownloadConfirm.setToolTip('i hope the program will not crash if you typed something wrong')
        self.directDownloadConfirm.clicked.connect(self.directDownload)
        
        self.directDownloadOutputLabel = DefaultLabel('Output:')
        self.directDownloadLayout.setWidget(3, ItemRole.LabelRole, self.directDownloadOutputLabel)
        self.directDownloadOutputLabel.setToolTip('Output of the performed action')
        
        self.directDownloadOutput = DefaultLabel()
        self.directDownloadLayout.setWidget(3, ItemRole.FieldRole, self.directDownloadOutput)
        self.directDownloadOutput.setToolTip('Output of the performed action')


        self.createListWidget = QtWidgets.QGroupBox()
        self.gridLayout.addWidget(self.createListWidget, 2, 1, 1, 2)
        self.createListWidget.setTitle('Create a search list')

        self.createListLayout = QtWidgets.QFormLayout(self.createListWidget)
        
        self.createListURL = QtWidgets.QLineEdit()
        self.createListLayout.setWidget(0, ItemRole.SpanningRole, self.createListURL)
        self.createListURL.setPlaceholderText('URL of the site with the books (with urls to them)')
        self.createListURL.setToolTip('For example https://azcomix.me/comic-list?c=t')
        
        self.createListOuterSelector = QtWidgets.QLineEdit()
        self.createListLayout.setWidget(1, ItemRole.SpanningRole, self.createListOuterSelector)
        self.createListOuterSelector.setPlaceholderText('CSS selector that grabs the books that have `href` attribute')
        self.createListOuterSelector.setToolTip('If you do not know how to get this, you should check out the Help tab')
        
        self.createListURLSuffix = QtWidgets.QLineEdit()
        self.createListLayout.setWidget(2, ItemRole.SpanningRole, self.createListURLSuffix)
        self.createListURLSuffix.setPlaceholderText('URL suffix to add to each issue url to make sure every image is on one page')
        self.createListURLSuffix.setToolTip('For example /full')
        
        self.createListSelector = QtWidgets.QLineEdit()
        self.createListLayout.setWidget(3, ItemRole.SpanningRole, self.createListSelector)
        self.createListSelector.setPlaceholderText('CSS selector that grabs the issues that have `href` attribute')
        self.createListSelector.setToolTip('If you do not know how to get this, you should check out the Help tab')
        
        self.createListInnerSelector = QtWidgets.QLineEdit()
        self.createListLayout.setWidget(4, ItemRole.SpanningRole, self.createListInnerSelector)
        self.createListInnerSelector.setPlaceholderText('CSS selector that grabs the images with `src` attribute in each issue')
        self.createListInnerSelector.setToolTip('If you do not know how to get this, you should check out the Help tab')

        self.createListConfirm = QtWidgets.QPushButton()
        self.createListLayout.setWidget(5, ItemRole.SpanningRole, self.createListConfirm)
        self.createListConfirm.setText('Attempt to create a list')
        self.createListConfirm.setToolTip('i hope the program will not crash if you typed something wrong')
        self.createListConfirm.clicked.connect(self.createList)
        
        self.createListOutputLabel = DefaultLabel('Output:')
        self.createListLayout.setWidget(6, ItemRole.LabelRole, self.createListOutputLabel)
        self.createListOutputLabel.setToolTip('Output of the performed action')
        
        self.createListOutput = DefaultLabel()
        self.createListLayout.setWidget(6, ItemRole.FieldRole, self.createListOutput)
        self.createListOutput.setToolTip('Output of the performed action')


    def addToLibrary(self):
        url = self.addToLibraryURL.text()

        selector = self.addToLibrarySelector.text()
        if selector == '':
            selector = None

        innerSelector = self.addToLibraryInnerSelector.text()
        if innerSelector == '':
            innerSelector = None

        urlSuffix = self.addToLibraryURLSuffix.text()

        success = LibraryUtils.addToLibrary(url, selector, innerSelector, urlSuffix)

        out = 'Success?' if success else 'FAILURE'

        self.addToLibraryOutput.setText(out)


        
    def directDownload(self):
        url = self.directDownloadURL.text()
        innerSelector = self.directDownloadInnerSelector.text()

        if innerSelector == '':
            innerSelector = None

        success = LocalUtils.directDownload(url, innerSelector)

        out = 'Success?' if success else 'FAILURE?'

        self.directDownloadOutput.setText(out)
        pass

    def createList(self):
        pass
