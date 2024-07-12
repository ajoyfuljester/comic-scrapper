from PySide6 import QtWidgets
from BrowserWidget import BrowserWidget
from SettingsWidget import SettingsWidget
from LibraryWidget import LibraryWidget
from HelpWidget import HelpWidget

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

        self.helpWidget = HelpWidget()
        self.addTab(self.helpWidget, 'Help')
        self.currentChanged.connect(self.handleTabChange)

    def handleTabChange(self, i):
        text = self.tabText(i)

        match text:
            case 'Help':
                self.widget(i).refresh()
