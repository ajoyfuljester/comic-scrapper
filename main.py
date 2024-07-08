from PySide6 import QtWidgets
from MainWidget import MainWidget
import ConfigUtils

config = ConfigUtils.loadConfig()

app = QtWidgets.QApplication()

mainWidget = MainWidget()
mainWidget.resize(800, 600)

if config['MAXIMIZE_WINDOW_ON_LAUNCH']:
    mainWidget.showMaximized()
else:
    mainWidget.show()

app.exec()
