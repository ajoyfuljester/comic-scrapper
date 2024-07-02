from PySide6 import QtWidgets
from MainWidget import MainWidget


app = QtWidgets.QApplication()

widget = MainWidget()
widget.resize(800, 600)
widget.show()

app.exec()
