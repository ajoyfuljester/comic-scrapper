from PySide6 import QtWidgets
from .QtUtils import *
from . import SettingsUtils
from .GenericWidgets import DefaultLabel


widgetInputMap = {
        'PATH_TO_LIBRARY': ['text', 'Path to a directory in the file system, where books will be stored'],
        'MAXIMIZE_WINDOW_ON_LAUNCH': ['checkbox', 'If window should be maximized, when the app is launched'],
        'INVERT_ISSUE_ORDER': ['checkbox', 'If order of issues in library should be inverted - ordered from oldest to newest'],
        'COLOR_BOOK_ALREADY_IN_LIBRARY': ['text', 'Color of a book in Browser, if the book is already in library'],
        'COLOR_ISSUE_ALREADY_DOWNLOADED': ['text', 'Color of an issue that is already downloaded'],
        'USE_SESSION': ['checkbox', 'If the tabs in Reader should be stored in a file after closing and loaded when the app is launched'],
        'COLOR_ISSUE_ALREADY_READ': ['text', 'Color of an issue that is already read'],
        'MARK_AS_READ_AFTER_LAST_PAGE': ['checkbox', 'If issues should be marked as read after showing the last page'],
        'COLOR_ISSUE_ALREADY_DOWNLOADED_AND_READ': ['text', 'Color of an issue that is already downloaded and read'],
        'NUMBER_OF_PAGES_TO_SCRAPE': ['number', 'Number of pages to scan, when searching in Browser (usually 25 book/page)'],
        'COLOR_ISSUE_DOWNLOAD_PENDING': ['text', 'Color of an issue that is being downloaded in the background'],
        'AUTO_REFRESH_LIBRARY': ['checkbox', 'If Library should be refreshed every time its tab is selected'],
        'AUTO_REFRESH_LOCAL': ['checkbox', 'If Local should be refreshed every time its tab is selected'],
        'FUSION_THEME': ['checkbox', 'If the app should use the fusion theme, it might be a dark theme'],
        'COLOR_ACCENT': ['text', 'Color of a few highlights, accents'],
        'COLOR_CELL': ['text', 'Color of a table cell, it is easier than programming dark theme'],
        'PATH_TO_LOCAL': ['text', 'Path to a directory in the file system, where books will be stored that do not have data.json file - usually books that were not downloaded using this app'],
        'SORT_TRIM_LEFT': ['number', 'Number of characters to trim from issue name from the left side to obtain its number (used for sorting) for example "book-121" would require the value of 5 to work properly'],
        'SORT_TRIM_RIGHT': ['number', 'Number of characters to trim from issue name from the right side to obtain its number (used for sorting) for example "13-issue" would require the value of 6 to work properly'],
}


class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.formLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(self.formLayout)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        
        self.settings = SettingsUtils.loadSettings()

        
        self.resetButton = QtWidgets.QPushButton('Reset')
        self.resetButton.clicked.connect(self.generateEditor)
        self.resetButton.setToolTip('Show currently saved settings')
        self.buttonLayout.addWidget(self.resetButton)
        self.generateEditor()

        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setText('Save')
        self.saveButton.setToolTip('Save changed settings')
        self.saveButton.clicked.connect(lambda _: (self.saveSettings(), self.generateEditor())) # This is cursed i hate this thing, but i don't want 2 lines 
        self.buttonLayout.addWidget(self.saveButton)


    def generateEditor(self):
        rowCount = self.formLayout.rowCount()
        for i in range(rowCount - 1, -1, -1): # not jumping indexes
            self.formLayout.itemAt(i, ItemRole.LabelRole).widget().deleteLater()
            self.formLayout.itemAt(i, ItemRole.FieldRole).widget().deleteLater()
            self.formLayout.removeRow(i)

        sortedSettings = sorted(self.settings.items(), key=lambda item: item[0])
        for key, value in sortedSettings:
            inputInfo = widgetInputMap[key]
            valueWidget = None
            match inputInfo[0]:
                case 'text':
                    valueWidget = QtWidgets.QLineEdit()
                    valueWidget.setText(value)
                    valueWidget.setPlaceholderText(value)
                    valueWidget.textChanged.connect(self.highlightChangedRows)
                case 'checkbox':
                    valueWidget = QtWidgets.QCheckBox()
                    valueWidget.setChecked(value)
                    valueWidget.checkStateChanged.connect(self.highlightChangedRows)
                case 'number':
                    valueWidget = QtWidgets.QSpinBox()
                    valueWidget.setValue(value)
                    valueWidget.valueChanged.connect(self.highlightChangedRows)
                case _:
                    raise Exception('Widget type not found!')


            valueWidget.setToolTip(inputInfo[1])

            keyWidget = DefaultLabel(key)
            keyWidget.setToolTip(inputInfo[1])

            self.formLayout.addRow(keyWidget, valueWidget)

        self.highlightChangedRows()


    def saveSettings(self):
        rowCount = self.formLayout.rowCount()
        for i in range(rowCount):
            key = self.formLayout.itemAt(i, ItemRole.LabelRole).widget().text()

            valueWidget = self.formLayout.itemAt(i, ItemRole.FieldRole).widget()
            value = self.getWidgetValue(valueWidget, key)


            self.settings[key] = value


        SettingsUtils.writeSettings(self.settings)
        self.highlightChangedRows()
    

        

    def highlightChangedRows(self):
        self.settings = SettingsUtils.loadSettings()
        changedKeyStylesheet = f"color: {self.settings['COLOR_ACCENT']};"
        changedValueStylesheet = changedKeyStylesheet
        rowCount = self.formLayout.rowCount()

        for i in range(rowCount):
            keyWidget = self.formLayout.itemAt(i, ItemRole.LabelRole).widget()
            key = keyWidget.text()
            valueWidget = self.formLayout.itemAt(i, ItemRole.FieldRole).widget()
            value = self.getWidgetValue(valueWidget, key)
            

            if self.settings[key] == value:
                keyWidget.setStyleSheet('')
                valueWidget.setStyleSheet('')
            else:
                keyWidget.setStyleSheet(changedKeyStylesheet)
                valueWidget.setStyleSheet(changedValueStylesheet)


            
    def getWidgetValue(self, valueWidget, key):
        value = None
        inputType = widgetInputMap[key][0]
        match inputType:
            case 'text':
                value = valueWidget.text()
            case 'checkbox':
                value = valueWidget.isChecked()
            case 'number':
                value = valueWidget.value()
            case _:
                raise Exception('Widget type not found!')
        
        return value




