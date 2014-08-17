import subprocess
import os
import sys
import tarfile

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

# os.chdir('c:/Users/jalbert/Downloads/clojars')

prefix = 'http://hackage.haskell.org'

subprocess.call(['wget', 'http://hackage.haskell.org/packages/index.tar.gz'])
allPackagesUrls = []
tf = tarfile.open('index.tar.gz')
for m in tf.getmembers():
    if str(m.name).endswith('.cabal'):
        parts = m.name.split('/')
        libName = parts[0]
        version = parts[1]
        name = libName + '-' + version
        allPackagesUrls.append(prefix + '/package/' + name + '/' + name + '.tar.gz')

open('allPackagesUrls.txt', 'w').write('\n'.join(allPackagesUrls))

os.mkdir('files')
subprocess.call(['cp', 'allPackagesUrls.txt', 'files/allPackagesUrls.txt'])
os.chdir('files')
subprocess.call(['wget', '-i', 'allPackagesUrls.txt'])

os.chdir('..')
os.mkdir('package')
# subprocess.call(['7z', 'x', 'index.tar.gz'])
# subprocess.call(['7z', 'x', '-y', '-o./index', 'index.tar'])

for m in tf.getmembers():
    if str(m.name).endswith('.cabal'):
        parts = m.name.split('/')
        libName = parts[0]
        version = parts[1]
        name = libName + '-' + version
        subprocess.call(['mkdir',  './package/' + name])
        subprocess.call(['mv', './files/' + name + '.tar.gz', './package/' + name])
        # copiar m (tar entry) en './package/' + name

# http://hackage.haskell.org/package/3d-graphics-examples-0.0.0.0/3d-graphics-examples-0.0.0.0.tar.gz
# http://hackage.haskell.org/package/3d-graphics-examples-0.0.0.0/3d-graphics-examples.cabal