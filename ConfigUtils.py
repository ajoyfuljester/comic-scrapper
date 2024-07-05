import json

def loadConfig():
    with open('settings.json') as file:
        config = json.loads(file.read())

    return config


def writeConfig(obj):
    s = json.dumps(obj)
    with open('settings.json', 'w') as file:
        file.write(s)

