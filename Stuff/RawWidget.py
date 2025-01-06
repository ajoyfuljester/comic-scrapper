from PySide6 import QtWidgets
from .GenericWidgets import DefaultLabel
from .QtUtils import *
from . import LibraryUtils


class RawWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.refresh()
    
    def refresh(self):
        self.addToLibraryWidget = QtWidgets.QGroupBox()
        self.gridLayout.addWidget(self.addToLibraryWidget, 1, 1)
        self.addToLibraryWidget.setTitle('Add to Library')

        self.addToLibraryLayout = QtWidgets.QFormLayout(self.addToLibraryWidget)
        
        self.addToLibraryURL = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(0, ItemRole.SpanningRole, self.addToLibraryURL)
        self.addToLibraryURL.setPlaceholderText('URL of the site with the issues')
        self.addToLibraryURL.setToolTip('For example https://azcomix.me/comic/the-sandman-1989')
        
        self.addToLibrarySelector = QtWidgets.QLineEdit()
        self.addToLibraryLayout.setWidget(1, ItemRole.SpanningRole, self.addToLibrarySelector)
        self.addToLibrarySelector.setPlaceholderText('CSS selector that grabs the things with `href`')
        self.addToLibrarySelector.setToolTip('If you do not know how to get this, you should check out the Help tab')
        self.addToLibraryConfirm = QtWidgets.QPushButton()
        self.addToLibraryLayout.setWidget(3, ItemRole.SpanningRole, self.addToLibraryConfirm)
        self.addToLibraryConfirm.setText('Attempt to add to Library')
        self.addToLibraryConfirm.setToolTip('i hope the program will not crash if you typed something wrong')
        self.addToLibraryConfirm.clicked.connect(self.addToLibrary)
        
        self.addToLibraryOutputLabel = DefaultLabel('Output:')
        self.addToLibraryLayout.setWidget(4, ItemRole.LabelRole, self.addToLibraryOutputLabel)
        self.addToLibraryOutputLabel.setToolTip('Output of the performed action')
        
        self.addToLibraryOutput = DefaultLabel()
        self.addToLibraryLayout.setWidget(4, ItemRole.FieldRole, self.addToLibraryOutput)
        self.addToLibraryOutput.setToolTip('Output of the performed action')


    def addToLibrary(self):
        url = self.addToLibraryURL.text()
        selector = self.addToLibrarySelector.text()

        if selector == '':
            selector = None


        success = LibraryUtils.addToLibrary(url, selector)

        out = 'Success?' if success else 'FAILURE'

        self.addToLibraryOutput.setText(out)


        
