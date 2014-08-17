import urllib.request
import subprocess
import os
import sys

from bs4 import BeautifulSoup

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

def fetchUrl(url):
    resp = urllib.request.urlopen(url)
    data = resp.read()
    t = data.decode('utf-8')
    s = BeautifulSoup(t)
    return t, s

os.chdir('c:/Users/jalbert/Downloads/clojars')
gHome = 0
sHome = 0
gAllPackages = 0
sAllPackages = 0
gAllPackagesVersions = 1
sAllPackagesVersions = 0

prefix = 'http://hackage.haskell.org'
if gHome:
    text, soup = fetchUrl(prefix + "/packages/names")
    if sHome:
        open('data.html', 'w').write(text)
        os._exit(0)
else:
    text = '\n'.join(open('data.html').readlines())
    soup = BeautifulSoup(text)

allPackages = []
if gAllPackages:
    for package in soup.find_all('ul')[1].find_all('li'):
        allPackages.append(prefix + package.a['href'])
    if sAllPackages:
        open('allPackages.txt', 'w').write('\n'.join(allPackages))
        os._exit(0)
else:
    allPackages = open('allPackages.txt').readlines()[:2]

allPackagesVersions = []
if gAllPackagesVersions:
    for p1 in allPackages:
        print(p1)
        text, soup = fetchUrl(p1)
        # for pversion in soup.find_all('table')[0]['tbody']['tr']['td']['a']:
        for pversion in soup.find_all('table'):
            # allPackagesVersions.append(pversion['href'])
            print('Tabla')
            for x in pversion.tr.td:
                print(x)

    if sAllPackagesVersions:
        open('allPackagesVersions.txt', 'w').write('\n'.join(allPackagesVersions))
        os._exit(0)
else:
    allPackagesVersions = open('allPackagesVersions.txt').readlines()[:20]

allPackagesUrls = []
for p1 in allPackagesVersions:
    text, soup = fetchUrl(p1)
    for pversion in soup.find_all('a'):
        href = str(pversion['href'])
        if href.endswith('.tar.gz') or href.endswith('.cabal'):
            allPackagesUrls.append(prefix + href)

open('allPackagesUrls.txt', 'w').write('\n'.join(allPackagesUrls))

# subprocess.call(['wget', '-i', 'allPackagesUrls.txt'])