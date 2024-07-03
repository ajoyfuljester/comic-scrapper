from PySide6 import QtWidgets
from BrowserWidget import BrowserWidget
from SettingsWidget import SettingsWidget

class MainWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.browserWidget = BrowserWidget()
        self.addTab(self.browserWidget, 'Browser')
        self.browserWidget.search.setFocus()


        self.settingsWidget = SettingsWidget()
        self.addTab(self.settingsWidget, 'Settings')


