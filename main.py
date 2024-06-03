from PySide6 import QtCore, QtWidgets, QtGui
import sys



class DownloadWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.search = QtWidgets.QLineEdit()
        self.results = QtWidgets.QTableWidget()
        self.results.setColumnCount(5)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.results)



class ComicTableWidgetItemSet():
    def __init__(self, entry):

        self.cellData = []

        self.cellData.append(entry['title'])
        self.cellData.append(entry['status'])
        self.cellData.append(entry['releaseDate'])
        self.cellData.append(entry['latest'])

        self.cellWidgets = [QtWidgets.QTableWidgetItem(cell) for cell in cellData]


        



app = QtWidgets.QApplication([])

widget = DownloadWidget()
widget.resize(800, 600)
widget.show()

app.exec()