from PySide6 import QtCore, QtWidgets, QtGui
import scrappingutils as su

Flags = QtCore.Qt.ItemFlag
Alignment = QtCore.Qt.AlignmentFlag
ResizeMode = QtWidgets.QHeaderView.ResizeMode
KeepAspectRatio = QtCore.Qt.AspectRatioMode.KeepAspectRatio

class DownloadWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.search = QtWidgets.QLineEdit()
        self.search.returnPressed.connect(self.searchComics)

        self.results = QtWidgets.QTableWidget()
        self.results.setColumnCount(4)
        self.results.setHorizontalHeaderLabels(['Title', 'Status', 'Release Date', 'Latest Issue'])
        tableHeader = self.results.horizontalHeader()
        tableHeader.setSectionResizeMode(0, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(1, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(2, ResizeMode.ResizeToContents)
        tableHeader.setSectionResizeMode(3, ResizeMode.Stretch)


        self.results.itemClicked.connect(self.handleItemClick)

        self.comicData = []

        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.leftColumn = QtWidgets.QVBoxLayout()
        self.rightGrid = QtWidgets.QGridLayout()
        self.gridLayout.addLayout(self.leftColumn, 0, 0)
        self.gridLayout.addLayout(self.rightGrid, 0, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.leftColumn.addWidget(self.search)
        self.leftColumn.addWidget(self.results)


    def searchComics(self):
        query = self.search.text()

        self.comicData = su.search(query, True)

        entryWidgets = [ComicTableWidgetItemSet(entry) for entry in self.comicData]
        self.results.setRowCount(0)

        for entryWidget in entryWidgets:
            entryWidget.appendSelf(self.results)

    def loadPreview(self, data):
        self.preview = ComicPreview(data)
        last = self.rightGrid.itemAtPosition(1, 0)
        if last:
            last.widget().deleteLater()
        self.rightGrid.addWidget(self.preview, 1, 0)
        self.preview.show()

        size = self.preview.size()
        descSize = self.preview.description.size()
        margins = self.preview.columnLayout.contentsMargins()
        descSize.setWidth(margins.left() + margins.right())
        descSize.setHeight(descSize.height() + self.rightGrid.verticalSpacing() + margins.top() + margins.bottom())
        size -= descSize

        self.preview.resizeCover(size)



    def handleItemClick(self, item):
        row = item.row()
        data = self.comicData[row]

        self.loadPreview(data)


class ComicTableWidgetItemSet():
    def __init__(self, entry):

        self.cellData = [
            entry['title'],
            entry['status'],
            entry['releaseDate'],
            entry['latest'],
        ]

        self.cellWidgets = [QtWidgets.QTableWidgetItem(cell) for cell in self.cellData]
        for cell in self.cellWidgets:
            cell.setFlags(Flags.ItemIsSelectable | Flags.ItemIsEnabled)

    
    def appendSelf(self, target):
        lastRow = target.rowCount()
        target.setRowCount(lastRow + 1)
        for i, cell in enumerate(self.cellWidgets):
            target.setItem(lastRow, i, cell)


class ComicPreview(QtWidgets.QWidget):
    def __init__(self, info):
        super().__init__()


        
        keys = list(info.keys())


        if 'imageURL' in keys or 'image' in keys:
            self.coverLabel = QtWidgets.QLabel()
            self.coverLabel.setAlignment(Alignment.AlignCenter)

            self.coverLabel.setMinimumSize(100, 100)
            self.coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding))
            #coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored))


            info['image'] = info.get('image') or su.getImageBytes(info['imageURL'])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info['image'])
            self.coverLabel.setPixmap(pixmap)
            if 'imageURL' in keys:
                keys.remove('imageURL')
            if 'image' in keys:
                keys.remove('image')



        self.columnLayout = QtWidgets.QVBoxLayout(self)
        self.columnLayout.addWidget(self.coverLabel)


        d = {}

        for key in keys:
            d[key] = info[key]


        self.description = DescriptionWidget(d)
        self.columnLayout.addWidget(self.description)



    
        
    def resizeCover(self, size):
        pixmap = self.coverLabel.pixmap()
        pixmap = pixmap.scaled(size, KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.coverLabel.setPixmap(pixmap)

        

class DescriptionWidget(QtWidgets.QWidget):
    def __init__(self, entries = {}):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setHorizontalSpacing(30)
        
        for k, v in entries.items():
            valueLabel = QtWidgets.QLabel(v)
            valueLabel.setWordWrap(True)
            self.formLayout.addRow(k.upper(), valueLabel)


app = QtWidgets.QApplication([])

widget = DownloadWidget()
#widget.resize(640, 480)
widget.resize(800, 600)



widget.show()
app.exec()
