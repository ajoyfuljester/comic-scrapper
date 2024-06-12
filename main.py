from PySide6 import QtCore, QtWidgets
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




        self.VLayout = QtWidgets.QVBoxLayout(self)
        self.VLayout.addWidget(self.search)
        self.VLayout.addWidget(self.results)

    def searchComics(self):
        query = self.search.text()

        entries = su.search(query)

        entryWidgets = [ComicTableWidgetItemSet(entry) for entry in entries]
        self.results.setRowCount(0)

        for entryWidget in entryWidgets:
            entryWidget.appendSelf(self.results)


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
