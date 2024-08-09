import json

def loadSettings():
    with open('settings.json') as file:
        settings = json.loads(file.read())

    return settings


def writeSettings(obj):
    s = json.dumps(obj, indent=4)
    with open('settings.json', 'w') as file:
        file.write(s)

