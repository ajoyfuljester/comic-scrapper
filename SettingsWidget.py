from PySide6 import QtWidgets
from QtUtils import *
import ConfigUtils


widgetInputMap = {
        'PATH_TO_LIBRARY': 'text',
        'MAXIMIZE_WINDOW_ON_LAUNCH': 'checkbox',
}


class SettingsWidget(QtWidgets.QWidget):
    defaultKeyStylesheet = 'color: black;'
    defaultValueStylesheet = 'color: black; placeholder-text-color: green;'
    changedKeyStylesheet = defaultKeyStylesheet + 'color: blue;'
    changedValueStylesheet = defaultValueStylesheet + 'color: blue;'
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.formLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(self.formLayout)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        
        self.config = ConfigUtils.loadConfig()

        def generateEditor():
            rowCount = self.formLayout.rowCount()
            if rowCount != 0:
                for i in range(rowCount - 1, -1, -1): # not jumping indexes
                    self.formLayout.itemAt(i, ItemRole.LabelRole).widget().deleteLater()
                    self.formLayout.itemAt(i, ItemRole.FieldRole).widget().deleteLater()
                    self.formLayout.removeRow(i)
            for key, value in self.config.items():
                inputType = widgetInputMap[key]
                valueWidget = None
                match inputType:
                    case 'text':
                        valueWidget = QtWidgets.QLineEdit()
                        valueWidget.setText(value)
                        valueWidget.setPlaceholderText(value)
                        valueWidget.textChanged.connect(self.highlightChangedRows)
                    case 'checkbox':
                        valueWidget = QtWidgets.QCheckBox()
                        valueWidget.setChecked(value)
                        valueWidget.checkStateChanged.connect(self.highlightChangedRows)
                    case _:
                        raise Exception('Widget type not found!')
                    
            
                keyWidget = QtWidgets.QLabel(key)
                keyWidget.setStyleSheet(self.defaultKeyStylesheet)
                valueWidget.setStyleSheet(self.defaultValueStylesheet)

                self.formLayout.addRow(keyWidget, valueWidget)

            self.highlightChangedRows()

        
        self.resetButton = QtWidgets.QPushButton('Reset')
        self.resetButton.clicked.connect(generateEditor)
        self.buttonLayout.addWidget(self.resetButton)
        generateEditor()

        





        def saveConfig():
            rowCount = self.formLayout.rowCount()
            for i in range(rowCount):
                key = self.formLayout.itemAt(i, ItemRole.LabelRole).widget().text()

                valueWidget = self.formLayout.itemAt(i, ItemRole.FieldRole).widget()
                value = self.getWidgetValue(valueWidget, widgetInputMap[key])
                

                self.config[key] = value


            ConfigUtils.writeConfig(self.config)
            self.highlightChangedRows()



        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.clicked.connect(lambda _: (saveConfig(), generateEditor())) # This is cursed i hate this thing, but i don't want 2 lines 
        self.buttonLayout.addWidget(self.saveButton)

    

        

    def highlightChangedRows(self):
        rowCount = self.formLayout.rowCount()

        for i in range(rowCount):
            keyWidget = self.formLayout.itemAt(i, ItemRole.LabelRole).widget()
            key = keyWidget.text()
            valueWidget = self.formLayout.itemAt(i, ItemRole.FieldRole).widget()
            value = self.getWidgetValue(valueWidget, widgetInputMap[key])
            

            if self.config[key] == value:
                keyWidget.setStyleSheet(self.defaultKeyStylesheet)
                valueWidget.setStyleSheet(self.defaultValueStylesheet)
            else:
                keyWidget.setStyleSheet(self.changedKeyStylesheet)
                valueWidget.setStyleSheet(self.changedValueStylesheet)


            
    def getWidgetValue(self, valueWidget, inputType):
        value = None
        match inputType:
            case 'text':
                value = valueWidget.text()
            case 'checkbox':
                value = valueWidget.isChecked()
        
        return value




