from PySide6 import QtCore, QtWidgets, QtGui
import scrappingutils as su

Flags = QtCore.Qt.ItemFlag

class DownloadWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.search = QtWidgets.QLineEdit()
        self.search.returnPressed.connect(self.searchComics)

        self.results = QtWidgets.QTableWidget()
        self.results.setColumnCount(4)
        self.results.setHorizontalHeaderLabels(['Title', 'Status', 'Release Date', 'Latest Issue'])


        self.results.setColumnWidth(0, 200)
        self.results.setColumnWidth(1, 70)
        self.results.setColumnWidth(2, 30)
        self.results.setColumnWidth(3, 400)

        self.results.itemClicked.connect(self.handleItemClick)

        self.comicData = []

        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.leftColumn = QtWidgets.QVBoxLayout()
        self.rightGrid = QtWidgets.QGridLayout()
        self.gridLayout.addLayout(self.leftColumn, 0, 0)
        self.gridLayout.addLayout(self.rightGrid, 0, 1)

        self.leftColumn.addWidget(self.search)
        self.leftColumn.addWidget(self.results)
        

    def searchComics(self):
        query = self.search.text()

        self.comicData = su.search(query)

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

        coverLabel = QtWidgets.QLabel()


        if 'imageURL' in keys or 'image' in keys:
            info['image'] = info.get('image') or su.getImageBytes(info['imageURL'])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info['image'])
            coverLabel.setPixmap(pixmap)
            if 'imageURL' in keys:
                keys.remove('imageURL')
            if 'image' in keys:
                keys.remove('image')



        self.columnLayout = QtWidgets.QVBoxLayout(self)
        self.columnLayout.addWidget(coverLabel)

        self.formLayout = QtWidgets.QFormLayout()
        self.columnLayout.addLayout(self.formLayout)
        self.formLayout.setHorizontalSpacing(30)

        for key in keys:
            self.formLayout.addRow(key.upper(), QtWidgets.QLabel(info[key]))
    
        




app = QtWidgets.QApplication([])

widget = DownloadWidget()
widget.resize(800, 600)


widget.show()
app.exec()
