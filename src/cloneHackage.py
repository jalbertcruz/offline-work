# import urllib.request
import subprocess
import os
import sys

# from bs4 import BeautifulSoup
import tarfile

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

# def fetchUrl(url):
# resp = urllib.request.urlopen(url)
# data = resp.read()
# t = data.decode('utf-8')
# s = BeautifulSoup(t)
# return t, s

# os.chdir('c:/Users/jalbert/Downloads/clojars')

prefix = 'http://hackage.haskell.org'

subprocess.call(['wget', 'http://hackage.haskell.org/packages/index.tar.gz'])
allPackagesUrls = []
tf = tarfile.open('index.tar.gz')
for m in tf.getmembers():
    if str(m.name).endswith('.cabal'):
        parts = m.name.split('/')
        allPackagesUrls.append(
            prefix + '/package/' + parts[0] + '-' + parts[1] + '/' + parts[0] + '-' + parts[1] + '.tar.gz')
        # print(parts)
# problems = []
# good = []
# for url in allPackagesUrls:
#     try:
#         resp = urllib.request.urlopen(url)
#         good.append(url)
#         # size += int(resp.headers['content-length'])
#         # print(dict(resp.getheaders()))
#     except Exception as e:
#         print(e)
#         problems.append(e)
#         problems.append(url)

open('allPackagesUrls.txt', 'w').write('\n'.join(allPackagesUrls))
# open('allPackagesUrls.txt', 'w').write('\n'.join(good))
# print('With problems:', len(problems))
# print(problems)
# print('Ok:', len(good))

# try:
# resp = urllib.request.urlopen('http://hackage.haskell.org/packages/index.tar.gz')
# print('Tiene:', resp.headers['content-length'], 'bytes')
# except Exception as e:
#     print(e)
os.mkdir('files')
subprocess.call(['cp', 'allPackagesUrls.txt', 'files/allPackagesUrls.txt'])
os.chdir('files')
subprocess.call(['wget', '-i', 'allPackagesUrls.txt'])