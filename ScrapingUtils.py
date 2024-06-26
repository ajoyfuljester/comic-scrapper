import requests
from bs4 import BeautifulSoup
import os




def getSources(url, max = None):
    response = requests.get(url)

    html = BeautifulSoup(response.text, 'html.parser')
    images = html.select('.chapter-container img')
    imagesLen = len(images)
    max = max or imagesLen

    sources = []
    i = 0
    while i < max and i < imagesLen:
        sources.append(images[i]['src'])
        i += 1

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

def getIssues(url, max = None):
    html = BeautifulSoup(requests.get(url).text, 'html.parser')

    rows = html.select('.episode-list tr')
    rowsLen = len(rows)
    max = max or rowsLen

    issues = []
    i = 0
    while i < max and i < rowsLen:
        issues.append({'name': rows[i].a.string, 'URL': rows[i].a['href']})
        i += 1

    return issues

    

def getAlternateImageURL(url, n = 1):
    return getSources(getIssues(url)[-n]['URL'], 1)[0]


def search(keyword='The Sandman', getAlternateImageURLs = False, getImages = False):
    url = 'https://comixextra.com/search'
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

            'status': details[1].string.split(': ')[1],
            'releaseDate': details[2].string.split(': ')[1],
            'latest': details[0].a.string,

            'URL': rawEntry.h3.a['href'],
            'imageURL': rawEntry.img['src'],
        }


        if getAlternateImageURLs and entry['imageURL'] == 'https://comixextra.com/images/sites/default.jpg':
            entry['imageURL'] = getAlternateImageURL(entry['URL'])


        entries.append(entry)
    
    if getImages:
        for entry in entries:
            entry['image'] = getImageBytes(entry['imageURL'])

    return entries

