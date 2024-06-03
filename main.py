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




app = QtWidgets.QApplication([])

widget = DownloadWidget()
widget.resize(800, 600)
widget.show()

app.exec()