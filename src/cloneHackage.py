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
        name = parts[0]
        version = parts[1]
        nameAndVersion = name + '-' + version
        allPackagesUrls.append(prefix + '/package/' + nameAndVersion + '/' + nameAndVersion + '.tar.gz')
        allPackagesUrls.append(prefix + '/package/' + nameAndVersion + '/' + name + '.cabal')

        #http://hackage.haskell.org/package/3d-graphics-examples-0.0.0.0/3d-graphics-examples-0.0.0.0.tar.gz
        #http://hackage.haskell.org/package/3d-graphics-examples-0.0.0.0/3d-graphics-examples.cabal

open('allPackagesUrls.txt', 'w').write('\n'.join(allPackagesUrls))

os.mkdir('files')
subprocess.call(['mv', 'allPackagesUrls.txt', 'files'])
os.chdir('files')
subprocess.call(['wget', '-i', 'allPackagesUrls.txt'])

os.chdir('..')
os.mkdir('package')
# subprocess.call(['7z', 'x', 'index.tar.gz'])
# subprocess.call(['7z', 'x', '-y', '-o./index', 'index.tar'])

for m in tf.getmembers():
    if str(m.name).endswith('.cabal'):
        parts = m.name.split('/')
        name = parts[0]
        version = parts[1]
        nameAndVersion = name + '-' + version
        subprocess.call(['mkdir', './package/' + nameAndVersion])
        subprocess.call(['mv', './files/' + nameAndVersion + '.tar.gz', './package/' + nameAndVersion])

subprocess.call(['mv', 'index.tar.gz', 'package'])