import json
import os


def saveSession(data):
    with open('session.json', 'w') as file:
        file.write(json.dumps(data, indent=4))


def loadSession():
    if not os.path.exists('session.json'):
        return {'reading': []}
    with open('session.json', 'r') as file:
        return json.loads(file.read())
