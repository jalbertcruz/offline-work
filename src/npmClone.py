import json
import subprocess
import gzip
import os
import collections
import tarfile

subprocess.call(['mkdir', 'npm'])
os.chdir('npm')


def prepare():
    subprocess.call(
        ['wget', 'http://nipster.blob.core.windows.net/cdn/npm-datatables.json', '-O', 'npm-datatables.json.gz'])
    open('npm-datatables.json', "wb").write(gzip.GzipFile('npm-datatables.json.gz', 'rb').read())
    subprocess.call(['node', '../readRepos.js'])
    data = json.loads("".join(open("repos.json").readlines()))
    data = list(set(data))
    open('repos.txt', "w").write('|'.join(data))
    names = [l[-1] for l in [e.split('/') for e in data]]
    duplicados = [x for x, y in collections.Counter(names).items() if y > 1]
    open('duplicados.txt', "w").write('\n'.join(duplicados))


def cloneRepos(n, m):
    data = open('repos.txt').readline().split('|')
    for d in data[n:m]:
        if d[-1] == '\n':
            d = d[:-1]
        e = d.split('/')
        user = e[-2]
        repo = e[-1]
        subprocess.call(['mkdir', user])
        os.chdir(user)
        subprocess.call(['git', 'clone', d])
        os.chdir(repo)
        s = subprocess.check_output(['git', 'tag'], universal_newlines=True, stderr=subprocess.STDOUT)
        versions = s.split('\n')
        versions = [v.strip() for v in versions if v.strip() != '']
        for v in versions:
            subprocess.call(['git', 'archive', '-o', '../' + repo + '-' + v + '.zip', v])
        os.chdir('..')
        tf = tarfile.open(repo + '.tar.gz', 'w:gz')
        tf.add(repo)
        tf.close()
        subprocess.call(['rm', '-R', repo])
        os.chdir('..')


def cloneAllRepos():
    data = open('repos.txt').readline().split('|')
    cloneRepos(0, len(data))


# cloneRepos(0, 3)
def downloadAll():
    prepare()
    cloneAllRepos()
    os.chdir('..')
    tf = tarfile.open('npm.tar.gz', 'w:gz')
    tf.add('npm')
    tf.close()
    subprocess.call(['rm', '-R', 'npm'])


def checkDependencies():
    data = open('repos.txt').readline().split('|')
    allRepos = set()
    for d in data:
        e = d.split('/')
        user = e[-2]
        repo = e[-1]
        subprocess.call(['mkdir', user])
        os.chdir(user)
        subprocess.call(['mkdir', repo])
        os.chdir(repo)
        subprocess.call(
            ['wget', '--no-check-certificate', 'https://raw.github.com/' + user + '/' + repo +'/master/package.json'])
        if os.path.isfile("package.json"):
            pk = json.loads("".join(open("package.json").readlines()))
            if 'name' in pk:
                allRepos.add(pk['name'])
        os.chdir('..')
        os.chdir('..')
    missing = set()
    for d in data:
        e = d.split('/')
        user = e[-2]
        repo = e[-1]
        os.chdir(user)
        os.chdir(repo)
        if os.path.isfile("package.json"):
            pk = json.loads("".join(open("package.json").readlines()))
            deps = set()
            if 'dependencies' in pk:
                for k in pk['dependencies']:
                    deps.add(k)
            if 'devDependencies' in pk:
                for k in pk['devDependencies']:
                    deps.add(k)
            missing.update(deps - allRepos)
        os.chdir('..')
        os.chdir('..')
    open('missing.txt', 'w').write('\n'.join(missing))

# downloadAll()
# prepare()
checkDependencies()