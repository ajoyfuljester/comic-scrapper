from PySide6 import QtWidgets
import json


class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)

        
        with open('settings.json') as file:
            config = json.loads(file.read())

        
        for k, v in config.items():
            print(k, v)
            self.formLayout.addRow(k, QtWidgets.QLabel(v))

        print(self.formLayout.rowCount())
