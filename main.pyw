from PySide6 import QtWidgets
from Stuff import SettingsUtils, SessionUtils
from Stuff.MainWidget import MainWidget

if __name__ == '__main__':

    settings = SettingsUtils.loadSettings()

    app = QtWidgets.QApplication()


    if settings['FUSION_THEME']:
        app.setStyle('fusion')

    mainWidget = MainWidget()
    mainWidget.resize(800, 600)

    if settings['MAXIMIZE_WINDOW_ON_LAUNCH']:
        mainWidget.showMaximized()
    else:
        mainWidget.show()

    if settings['USE_SESSION']:
        data = SessionUtils.loadSession()
        for reading in data['reading']:
            mainWidget.readerWidget.addReaderTab(reading['title'], reading['issue'], reading['pageNumber'])

    app.exec()

    settings = SettingsUtils.loadSettings()

    if settings['USE_SESSION']:
        numberOfTabs = mainWidget.readerWidget.count()
        data = {'reading': []}
        for i in range(numberOfTabs):
            tab = mainWidget.readerWidget.widget(i)
            data['reading'].append({'title': tab.title, 'issue': tab.issue, 'pageNumber': tab.currentPageNumber})

        SessionUtils.saveSession(data)
