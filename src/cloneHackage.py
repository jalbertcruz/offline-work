import urllib.request
import subprocess
import os
import sys

from bs4 import BeautifulSoup

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

prefix = 'http://hackage.haskell.org'
resp = urllib.request.urlopen(prefix + "/packages/names")
data = resp.read()
text = data.decode('utf-8')
soup = BeautifulSoup(text)

allPackages = []
for i in soup.find_all('ul')[1].find_all('li'):
    allPackages.append(prefix + i.a['href'])

allPackagesUrls = []
for e in allPackages:
    resp = urllib.request.urlopen(e)
    data = resp.read()
    text = data.decode('utf-8')
    soup = BeautifulSoup(text)
    for i in soup.find_all('a'):
        href = str(i['href'])
        if href.endswith('.tar.gz'):
            allPackagesUrls.append(prefix + href)

open('allPackagesUrls.txt', 'w').write('\n'.join(allPackagesUrls))

subprocess.call(['wget', '-i', 'allPackagesUrls.txt'])