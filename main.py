from PySide6 import QtWidgets
from DownloadWidget import DownloadWidget

app = QtWidgets.QApplication()

widget = DownloadWidget()
widget.resize(800, 600)
widget.show()

app.exec()
