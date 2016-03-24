from bs4 import BeautifulSoup
import requests
import os

baseUrl = "http://www.midiworld.com/search/"
baseOutpath = "C:\Users\Debbie\Desktop\MidiScraping\\"
mbyte = 1024 * 1024

genres = ['classic','pop','rock','rap','dance','punk','blues','country','jazz','hip-hop']
stopPage = 'found nothing!'
for genre in genres:
    pageNumber = 1
    firstUrl = baseUrl + str(pageNumber) + '/?q=' + genre
    print 'Starting: ', firstUrl
    html = requests.get(firstUrl).text
    soup = BeautifulSoup(html, "lxml")
    while stopPage not in soup.get_text():
        for name in soup.findAll('a', href=True):
            midurl = name['href']
            if '/download/' in midurl:
                outFName = baseOutpath + genre + '\\' + midurl.split('/')[-1] + '.midi'
                outDir = os.path.dirname(outFName)
                if not os.path.exists(outDir):
                    os.makedirs(outDir)
                r = requests.get(midurl, stream=True)
                if r.status_code == requests.codes.ok:
                    fsize = int(r.headers['content-length'])
                    print 'Downloading %s (%sMb)' % (outFName, fsize / mbyte)
                    with open(outFName, 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=1024):  # chuck size can be larger
                            if chunk:  # ignore keep-alive requests
                                fd.write(chunk)
                        fd.close()
        pageNumber += 1
        nextUrl = baseUrl + str(pageNumber) + '/?q=' + genre
        print 'Starting: ', nextUrl
        html = requests.get(nextUrl).text
        soup = BeautifulSoup(html, "lxml")
