from PySide6 import QtWidgets
from .BrowserWidget import BrowserWidget
from .SettingsWidget import SettingsWidget
from .LibraryWidget import LibraryWidget
from .LocalWidget import LocalWidget
from .HelpWidget import HelpWidget
from .ReaderWidget import ReaderWidget
from .RawWidget import RawWidget
from . import SettingsUtils

class MainWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.settings = SettingsUtils.loadSettings()

        self.browserWidget = BrowserWidget()
        self.addTab(self.browserWidget, 'Browser')
        self.browserWidget.searchInput.setFocus()

        self.rawWidget = RawWidget()
        self.addTab(self.rawWidget, 'Raw')

        self.readerWidget = ReaderWidget()

        self.libraryWidget = LibraryWidget(self.readerWidget)
        self.addTab(self.libraryWidget, 'Library')

        self.localWidget = LocalWidget(self.readerWidget)
        self.addTab(self.localWidget, 'Local')

        self.addTab(self.readerWidget, 'Reader')

        self.settingsWidget = SettingsWidget()
        self.addTab(self.settingsWidget, 'Settings')

        self.helpWidget = HelpWidget()
        self.addTab(self.helpWidget, 'Help')

        self.currentChanged.connect(self.handleTabChange)

        self.setWindowTitle('Comic Scraper')


    def handleTabChange(self, i):
        self.settings = SettingsUtils.loadSettings()

        text = self.tabText(i)

        match text:
            case 'Help':
                self.widget(i).refresh()
            case 'Library':
                if self.settings['AUTO_REFRESH_LIBRARY']:
                    self.widget(i).refresh()
            case 'Local':
                if self.settings['AUTO_REFRESH_LOCAL']:
                    self.widget(i).refresh()
