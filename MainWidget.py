from PySide6 import QtWidgets
from BrowserWidget import BrowserWidget
from SettingsWidget import SettingsWidget
from LibraryWidget import LibraryWidget

class MainWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.browserWidget = BrowserWidget()
        self.addTab(self.browserWidget, 'Browser')
        self.browserWidget.searchInput.setFocus()

        self.libraryWidget = LibraryWidget()
        self.addTab(self.libraryWidget, 'Library')

        self.settingsWidget = SettingsWidget()
        self.addTab(self.settingsWidget, 'Settings')
