import requests
from bs4 import BeautifulSoup
import os



def getSources(url, max = None, selector = None):
    if selector == None:
        selector = '.chapter-container img'
    response = requests.get(url)

    html = BeautifulSoup(response.text, 'html.parser')
    images = html.select(selector)
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
    source = source.strip()
    response = requests.get(source)
    imageBytes = response.content
    return imageBytes



def saveSource(source, path='./', name='_'):
    if path[-1] != '/':
        path += '/'
    os.makedirs(path, exist_ok=True)
    
    filename = path + str(name)

    with open(filename, 'wb') as file:
        file.write(getImageBytes(source))



def saveSources(sources, path='./', names=None):
    if path[-1] != '/':
        path += '/'

    if names == None:
        names = [str(i) + '.png' for i in range(len(sources))]

    for i, source in enumerate(sources):
        saveSource(source, path, names[i])

def getIssues(url, max = None, customSelector = '.basic-list li > a'):
    html = BeautifulSoup(requests.get(url).text, 'html.parser')

    return getIssuesBS(html, max, customSelector)

def getIssuesBS(html, max = None, customSelector = '.basic-list li > a'):
    rows = html.select(customSelector)
    rowsLen = len(rows)
    max = max or rowsLen

    issues = []
    i = 0
    while i < max and i < rowsLen:
        issues.append({'name': rows[i].string, 'URL': rows[i]['href']})
        i += 1

    return issues

# OLD
# def getFullComicBookInfo(url):
#     response = requests.get(url)
#     html = BeautifulSoup(response.text, 'html.parser')
#     details = html.select_one('.movie-detail')
#     table = details.select('dd')
#     issues = getIssuesBS(html)
#     
#     imageURL = html.select_one('.movie-image').img['src']
#     info = {
#         'info': {
#             'title': details.select_one('.title-1').text.strip(),
#             'author': table[3].text.strip(),
#             'status': table[0].text.strip(),
#             'releaseYear': table[2].text.strip(),
#             'latest': issues[-1]['name'],
#             'URL': url,
#             'imageURL': imageURL,
#             'image': str(getImageBytes(imageURL).hex()),
#             'numberOfIssues': len(issues),
#             'genres': [{'name': el.text, 'URL': el['href']} for el in table[4].select('a')],
# 
#         },
#         'issues': issues,
#     }
# 
# 
# 
#     return info

def getFullComicBookInfo(url, customSelector = None):
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    if customSelector == None:
        details = html.select_one('.anime-details')
        table = details.select('.full-table tr td:nth-child(2)')
        issues = getIssuesBS(html)

        
        imageURL = html.select_one('.anime-image').img['src']
        info = {
            'info': {
                'title': details.select_one('.title').text.strip(),
                'author': table[3].text.strip(),
                'releaseYear': table[2].text.strip(),
                'latest': issues[-1]['name'],
                'URL': url,
                'imageURL': imageURL,
                'image': str(getImageBytes(imageURL).hex()),
                'numberOfIssues': len(issues),
                'genres': [{'name': el.text, 'URL': el['href']} for el in details.select('.anime-genres li > a')],

            },
            'issues': issues,
        }
    else:
        issues = getIssuesBS(html, None, customSelector)
        info = {
            'info': {
                'title': url.removeprefix('http://').removeprefix('https://'),
                'releaseYear': '0',
                'latest': issues[-1]['name'],
                'URL': url,
                'numberOfIssues': len(issues),
            },
            'issues': issues,
        }



    return info

def getAlternativeImageURL(url, n = 1, m = 0):
    return getSources(getIssues(url)[-n]['URL'] + '/full', m + 1)[m]


# OLD
# def search(keyword='The Sandman', page = 1, getAlternateImageURLs = False, getImages = False):
#     url = 'https://comixextra.com/search'
#     keyword = keyword.replace(' ', '+')
#     searchURL = url + '?keyword=' + keyword + '&page=' + str(page)
#     response = requests.get(searchURL)
# 
#     html = BeautifulSoup(response.text, 'html.parser')
#     rawEntries = html.select('.cartoon-box')
#     entries = []
# 
#     for rawEntry in rawEntries:
#         details = rawEntry.select('.detail')
#         
# 
#         
#         entry = {
#             'title': rawEntry.h3.string,
# 
#             'status': details[1].string.split(': ')[1],
#             'releaseYear': details[2].string.split(': ')[1],
#             'latest': details[0].a.string if details[0].a != None else '',
# 
#             'URL': rawEntry.h3.a['href'],
#             'imageURL': rawEntry.img['src'],
#         }
# 
# 
#         if getAlternateImageURLs and entry['imageURL'] == 'https://comixextra.com/images/sites/default.jpg':
#             entry['imageURL'] = getAlternativeImageURL(entry['URL'])
# 
# 
#         entries.append(entry)
#     
#     if getImages:
#         for entry in entries:
#             entry['image'] = getImageBytes(entry['imageURL'])
# 
#     return entries

def search(keyword='The Sandman', getImages = False):
    url = 'https://azcomix.me/ajax/search?q='
    searchURL = url + keyword
    response = requests.get(searchURL)

    data = response.json()['data']

    entries = []

    for rawEntry in data:
        entry = {
            'title': rawEntry['title'],

            'URL': f"https://azcomix.me/comic/{rawEntry['slug']}",
            'imageURL': rawEntry['img_url'],
        }



        entries.append(entry)
    
    if getImages:
        for entry in entries:
            entry['image'] = getImageBytes(entry['imageURL'])

    return entries
