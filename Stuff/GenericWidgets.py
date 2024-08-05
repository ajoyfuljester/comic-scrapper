from PySide6 import QtWidgets, QtGui
from . import ScrapingUtils
from .QtUtils import *
import re


class ComicPreviewWidget(QtWidgets.QWidget):
    def __init__(self, info, verticalLayout = True):
        super().__init__()

        self.info = info


        
        keys = list(self.info.keys())


        if 'imageURL' in keys or 'image' in keys:
            self.info['image'] = self.info.get('image') or ScrapingUtils.getImageBytes(self.info['imageURL'])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self.info['image'])
            self.coverLabel = ResizingLabel(pixmap)
            self.coverLabel.setAlignment(Alignment.AlignCenter)

            self.coverLabel.setMinimumSize(100, 100)
            self.coverLabel.setSizePolicy(SizePolicy(SizePolicy.Policy.Minimum, SizePolicy.Policy.Minimum))
            if 'imageURL' in keys:
                keys.remove('imageURL')
            if 'image' in keys:
                keys.remove('image')



        if verticalLayout:
            self.childLayout = QtWidgets.QVBoxLayout(self)
        else:
            self.childLayout = QtWidgets.QHBoxLayout(self)

        self.childLayout.addWidget(self.coverLabel)
        self.sideLayout = QtWidgets.QVBoxLayout()
        self.childLayout.addLayout(self.sideLayout)


        d = {}
        hasGenres = 'genres' in keys

        if hasGenres:
            keys.remove('genres')

        for key in keys:
            d[key] = str(self.info[key])

        if hasGenres:
            d['genres'] = ", ".join(['<a href="' + genre['URL'] + '">' + genre['name'] + '</a>' for genre in self.info['genres']])

        self.description = DescriptionWidget(d)
        self.sideLayout.addWidget(self.description)


        self.alternativeImageNumber = -1
        self.getAlternativeImageButton = QtWidgets.QPushButton()
        self.getAlternativeImageButton.setText('Get alternative image')
        self.getAlternativeImageButton.setToolTip('Get first page of an issue')
        self.getAlternativeImageButton.clicked.connect(self.getAlternativeImage)
        self.sideLayout.addWidget(self.getAlternativeImageButton)


    def getAlternativeImage(self):
        self.alternativeImageNumber += 1
        url = ScrapingUtils.getAlternativeImageURL(self.info['URL'], 1, self.alternativeImageNumber)
        img = ScrapingUtils.getImageBytes(url)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(img)
        self.coverLabel._pixmap = pixmap
        self.coverLabel.resizeEvent({})


        
def createSpaces(string):
    if len(string) == 0 or string.isupper():
        return string

    spaces = []
    i = 1
    while i < len(string):
        if string[i].isupper():
            spaces.append(i)
        i += 1

    for i in reversed(spaces):
        string = string[:i] + ' ' + string[i:]

    return string

class DescriptionWidget(QtWidgets.QWidget):
    def __init__(self, entries = {}):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setHorizontalSpacing(30)

        linkPattern = re.compile(r'https:\/\/[a-zA-z\d\.]{1,}\/{0,1}')
        
        for k, v in entries.items():
            if linkPattern.match(v):
                v = f'<a href="{v}">{v}</a>'
            valueLabel = DefaultLabel(v)
            valueLabel.setOpenExternalLinks(True)
            valueLabel.setWordWrap(True)
            self.formLayout.addRow(DefaultLabel(createSpaces(k).upper()), valueLabel)

class DefaultLabel(QtWidgets.QLabel):
    def __init__(self, text = ''):
        super().__init__(text)
        self.setTextInteractionFlags(TextInteractionFlag.TextSelectableByMouse | TextInteractionFlag.LinksAccessibleByMouse | TextInteractionFlag.LinksAccessibleByKeyboard)

class ResizingLabel(QtWidgets.QLabel):
    def __init__(self, pixmap):
        super().__init__()
        self._pixmap = pixmap
        self.setPixmap(self._pixmap)

    def resizeEvent(self, event):
        pixmap = self._pixmap
        size = self.frameSize()
        self.setPixmap(pixmap.scaled(size, KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
