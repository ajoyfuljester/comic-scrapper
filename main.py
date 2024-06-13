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

        self.coverPreview = QtWidgets.QLabel()
        self.coverPixmap = QtGui.QPixmap()
        self.coverPreview.setPixmap(self.coverPixmap)


        self.GridLayout = QtWidgets.QGridLayout(self)
        self.GridLayout.addWidget(self.search, 0, 0)
        self.GridLayout.addWidget(self.results, 1, 0)
        self.GridLayout.addWidget(self.coverPreview, 1, 1)

    def searchComics(self):
        query = self.search.text()

        self.comicData = su.search(query)

        entryWidgets = [ComicTableWidgetItemSet(entry) for entry in self.comicData]
        self.results.setRowCount(0)

        for entryWidget in entryWidgets:
            entryWidget.appendSelf(self.results)

    def loadPreview(self, data):
        self.coverPixmap.loadFromData(data)
        self.coverPreview.setPixmap(self.coverPixmap)

    def handleItemClick(self, item):
        row = item.row()
        data = self.comicData[row]
        data['image'] = data.get('image') or su.getImageBytes(data['imageURL'])

        self.loadPreview(data['image'])


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


app = QtWidgets.QApplication([])

widget = DownloadWidget()
widget.resize(800, 600)


widget.show()
app.exec()
