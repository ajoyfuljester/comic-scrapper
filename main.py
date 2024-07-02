from PySide6 import QtWidgets
from BrowserWidget import BrowserWidget


class MainWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.browserWidget = BrowserWidget()


        self.addTab(self.browserWidget, 'Browser')
        self.browserWidget.search.setFocus()



app = QtWidgets.QApplication()

widget = MainWidget()
widget.resize(800, 600)
widget.show()

app.exec()
