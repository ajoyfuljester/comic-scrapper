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
            _ = self.formLayout.itemAt(i, ItemRole.LabelRole)
            if _:
                _.widget().deleteLater()
            _ = self.formLayout.itemAt(i, ItemRole.FieldRole)
            if _:
                _.widget().deleteLater()
            _ = self.formLayout.itemAt(i, ItemRole.SpanningRole)
            if _:
                _.widget().deleteLater()
            self.formLayout.removeRow(i)
        self.config = ConfigUtils.loadConfig()

        _ = DefaultLabel("How to use: go to Browser, search for a book, select a book, click button add to library, go to Library, select a book, select an issue, click button download, select an issue, click button read, go to Reader, click button next page if you want to see the next page")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

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

        _ = DefaultLabel("version v2.0")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)
