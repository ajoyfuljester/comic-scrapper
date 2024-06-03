import requests
from bs4 import BeautifulSoup
import os




def getSources(url='https://comixextra.com/the-sandman-1989/issue-1/full'):
    response = requests.get(url)

    html = BeautifulSoup(response.text, 'html.parser')
    images = html.select('.chapter-container img')

    sources = [image['src'] for image in images]

    return sources


def getMultipleSources(urls):
    return [getSources(url) for url in urls]


def getImageBytes(source):
    response = requests.get(source)
    imageBytes = response.content
    return imageBytes



def saveSource(source, path='./', name='_'):
    if path[-1] != '/':
        path += '/'
    os.makedirs(path, exist_ok=True)
    
    filename = path + name

    with open(filename, 'wb') as file:
        file.write(getImageBytes(source))



def saveSources(sources, path='./', names=None):
    if path[-1] != '/':
        path += '/'

    if names == None:
        names = range(len(sources))

    for i, source in enumerate(sources):
        saveSource(source, path, names[i])


def search(keyword='The Sandman', url='https://comixextra.com/search', getImages=False):
    keyword = keyword.replace(' ', '+')
    searchURL = url + '?keyword=' + keyword
    response = requests.get(searchURL)

    html = BeautifulSoup(response.text, 'html.parser')
    rawEntries = html.select('.cartoon-box')
    entries = []

    for rawEntry in rawEntries:
        details = rawEntry.select('.detail')

        entry = {
            'title': rawEntry.h3.string,

            'releaseDate': details[2].string.split(': ')[1],
            'status': details[1].string.split(': ')[1],
            'latest': details[0].a.string,

            'imageURL': rawEntry.img['src'],
        }

        entries.append(entry)
    
    if getImages:
        for entry in entries:
            entry['image'] = getImageBytes(entry['imageURL'])

    return entries

