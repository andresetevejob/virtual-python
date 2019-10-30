import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib


def init(repo):
    """Create directory for repo and initialize .git directory
       La commande git init cree trois dossiers qui sont objects,refs,refs/heads
       Elle cree ensuite un fichier HEAD qui va contenir la valeur ref:refs/heads/master
       C'est a dire que par defaut le HEAD pointe sur le master
    """
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.git'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.git', name))
    write_file(os.path.join(repo, '.git', 'HEAD'),
               b'ref:refs/heads/master')
    print('initialized empty repository: {}'.format(repo))


def write_file(path, data):
    """Write data bytes to file at given path"""
    with open(path, 'wb')as f:
        f.write(data)


def hash_object(data,obj_type,write=True):
    """ Compute hash of object data of given type and write to object store
    if "write" is True. Return SHA-1 object hash as hex string
    """
    header = '{}{}'.format(obj_type,len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest
    if write:
        path = os.path.join('.git','objects',sha1[:2],sha1[:1])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path),exist_ok=True)
            write_file(path,zlib.compress(full_data))
    return sha1

if __name__ == '__main__':
    init('gitInParticle')
