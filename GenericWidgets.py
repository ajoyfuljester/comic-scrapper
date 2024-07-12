from PySide6 import QtWidgets, QtGui
import ScrapingUtils
from QtUtils import *
import re


class ComicPreviewWidget(QtWidgets.QWidget):
    def __init__(self, info, verticalLayout = True):
        super().__init__()


        
        keys = list(info.keys())


        if 'imageURL' in keys or 'image' in keys:
            self.coverLabel = QtWidgets.QLabel()
            self.coverLabel.setAlignment(Alignment.AlignCenter)

            self.coverLabel.setMinimumSize(100, 100)
            self.coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum))
            #coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored))


            info['image'] = info.get('image') or ScrapingUtils.getImageBytes(info['imageURL'])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info['image'])
            self.coverLabel.setPixmap(pixmap)
            if 'imageURL' in keys:
                keys.remove('imageURL')
            if 'image' in keys:
                keys.remove('image')



        if verticalLayout:
            self.childLayout = QtWidgets.QVBoxLayout(self)
        else:
            self.childLayout = QtWidgets.QHBoxLayout(self)

        self.childLayout.addWidget(self.coverLabel)


        d = {}
        hasGenres = 'genres' in keys

        if hasGenres:
            keys.remove('genres')

        for key in keys:
            d[key] = str(info[key])

        if hasGenres:
            d['genres'] = ", ".join(['<a href="' + genre['URL'] + '">' + genre['name'] + '</a>' for genre in info['genres']])

        self.description = DescriptionWidget(d)
        self.childLayout.addWidget(self.description)



    
        
    def resizeCover(self, size):
        pixmap = self.coverLabel.pixmap()
        pixmap = pixmap.scaled(size, KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.coverLabel.setPixmap(pixmap)

        

class DescriptionWidget(QtWidgets.QWidget):
    def __init__(self, entries = {}):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setHorizontalSpacing(30)

        linkPattern = re.compile(r'https:\/\/[a-zA-z\d\.]{1,}\/{0,1}')
        
        for k, v in entries.items():
            if linkPattern.match(v):
                v = f'<a href="{v}">{v}</a>'
            valueLabel = QtWidgets.QLabel(v)
            valueLabel.setOpenExternalLinks(True)
            valueLabel.setWordWrap(True)
            valueLabel.setTextInteractionFlags(TextInteractionFlag.TextSelectableByMouse | TextInteractionFlag.LinksAccessibleByMouse | TextInteractionFlag.LinksAccessibleByKeyboard)
            self.formLayout.addRow(k.upper(), valueLabel)

