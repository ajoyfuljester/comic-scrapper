from PySide6 import QtWidgets
from Stuff import ConfigUtils, SessionUtils
from Stuff.MainWidget import MainWidget

config = ConfigUtils.loadConfig()

app = QtWidgets.QApplication()

mainWidget = MainWidget()
mainWidget.resize(800, 600)

if config['MAXIMIZE_WINDOW_ON_LAUNCH']:
    mainWidget.showMaximized()
else:
    mainWidget.show()

if config['USE_SESSION']:
    data = SessionUtils.loadSession()
    for reading in data['reading']:
        mainWidget.readerWidget.addReaderTab(reading['title'], reading['issue'], reading['pageNumber'])

app.exec()

config = ConfigUtils.loadConfig()

if config['USE_SESSION']:
    numberOfTabs = mainWidget.readerWidget.count()
    data = {'reading': []}
    for i in range(numberOfTabs):
        tab = mainWidget.readerWidget.widget(i)
        data['reading'].append({'title': tab.title, 'issue': tab.issue, 'pageNumber': tab.currentPageNumber})

    SessionUtils.saveSession(data)
