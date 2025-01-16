from PySide6 import QtWidgets
from .QtUtils import *
from . import SettingsUtils
from .GenericWidgets import DefaultLabel


class HelpWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setVerticalSpacing(12)

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
        self.settings = SettingsUtils.loadSettings()

        _ = DefaultLabel("How to use: go to Browser, search for a book, select a book, click button add to library, go to Library, select a book, select an issue, click button download, select an issue, click button read, go to Reader, click button next page if you want to see the next page")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("Books don't work after updating? Try deleting data.json file in each book directory and add them again to library (you will most likely loose your reading progress). Doing this does not ensure that the app will work")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("Resizing doesn't work/acts weird while window is not maximized? Try changing tabs (not Reader tabs) and resizing again. It sometimes works, i don't know what's going on or how to fix it, good luck")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("if you want something then create an <a href=\"https://github.com/ajoyfuljester/comic-scrapper/issues\">issue</a> on github or something, i have not used it so i don't know. if it is a bug, i might fix it, if it is a feature, then i will add it if i think it is cool or easy enough")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("CSS Selectors wiki or guide or something idk here you go: <a href=\"https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors\">full guide</a> but all you will probably need is <a href=\"https://developer.mozilla.org/en-US/docs/Web/CSS/Type_selectors\">type selectors</a>, <a href=\"https://developer.mozilla.org/en-US/docs/Web/CSS/Class_selectors\">class selectors</a>, <a href=\"https://developer.mozilla.org/en-US/docs/Web/CSS/ID_selectors\">id selectors</a> and <a href=\"https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator\">descendant combinator</a>... Good luck! i believe you can do it if you really try")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("if you write the wrong selector the program probably will not work, surprisingly though this program rarely crashes i suppose that's thanks to Pyside6")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)


        _ = DefaultLabel()
        color = self.settings['COLOR_BOOK_ALREADY_IN_LIBRARY']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of a comic book already in library'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_ISSUE_ALREADY_DOWNLOADED']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue already downloaded'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_ISSUE_ALREADY_READ']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue already read'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_ISSUE_ALREADY_DOWNLOADED_AND_READ']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue already downloaded and read'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_ISSUE_DOWNLOAD_PENDING']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of an issue that is being downloaded in the background (highlighting disappears when issues are refreshed)'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_ACCENT']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of a few highlights, accents'), _)

        _ = DefaultLabel()
        color = self.settings['COLOR_CELL']
        _.setStyleSheet(f'background-color: {color}')
        self.formLayout.addRow(DefaultLabel('color of a cell in a table'), _)

        _ = DefaultLabel("try hovering over buttons, most of them if not all have tooltips")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)

        _ = DefaultLabel("version v4.1")
        self.formLayout.setWidget(self.formLayout.rowCount(), ItemRole.SpanningRole, _)
