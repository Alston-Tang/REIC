__author__ = 'tang'

from hashlib import sha256


def encode(password):
    gen = sha256()
    gen.update(password)
    return gen.hexdigest()
