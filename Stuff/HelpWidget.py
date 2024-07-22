from PySide6 import QtWidgets
from .QtUtils import *
from . import ConfigUtils
from .GenericWidgets import DefaultLabel


class HelpWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)

        self.refresh()

    def refresh(self):
        rowCount = self.formLayout.rowCount()
        for i in range(rowCount - 1, -1, -1): # not jumping indexes
            self.formLayout.itemAt(i, ItemRole.LabelRole).widget().deleteLater()
            self.formLayout.itemAt(i, ItemRole.FieldRole).widget().deleteLater()
            self.formLayout.removeRow(i)
        self.config = ConfigUtils.loadConfig()

        _ = DefaultLabel()
        color = self.config['COLOR_BOOK_ALREADY_IN_LIBRARY']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of a comic book already in library'), _)

        _ = DefaultLabel()
        color = self.config['COLOR_ISSUE_ALREADY_DOWNLOADED']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue already downloaded'), _)

        _ = DefaultLabel()
        color = self.config['COLOR_ISSUE_ALREADY_READ']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue already read'), _)
