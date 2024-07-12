from PySide6 import QtWidgets
from QtUtils import *
import ConfigUtils


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

        _ = QtWidgets.QLabel()
        color = self.config['COLOR_COMIC_BOOK_ALREADY_IN_LIBRARY']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow('In Library', _)
