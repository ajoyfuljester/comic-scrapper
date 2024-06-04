from PySide6 import QtCore, QtWidgets
import sys
import scrappingutils as su

Flags = QtCore.Qt.ItemFlags

class DownloadWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.search = QtWidgets.QLineEdit()

        self.results = QtWidgets.QTableWidget()
        self.results.setColumnCount(4)
        self.results.setHorizontalHeaderLabels(['Title', 'Status', 'Release Date', 'Latest Issue'])


        tableWidth = self.results.width()
        self.results.setColumnWidth(0, 200)
        self.results.setColumnWidth(1, 70)
        self.results.setColumnWidth(2, 30)
        self.results.setColumnWidth(3, 400)




        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.results)



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

searchResults = su.search()

resultWidgets = [ComicTableWidgetItemSet(result) for result in searchResults] 

for row in resultWidgets:
    row.appendSelf(widget.results)

widget.show()
app.exec()