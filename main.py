from PySide6 import QtWidgets
from MainWidget import MainWidget
import ConfigUtils

config = ConfigUtils.loadConfig()

app = QtWidgets.QApplication()

widget = MainWidget()
widget.resize(800, 600)

if config['MAXIMIZE_WINDOW_ON_LAUNCH']:
    widget.showMaximized()
else:
    widget.show()

app.exec()
