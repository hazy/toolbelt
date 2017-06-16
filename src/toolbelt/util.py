import binascii
import os

def random_bytes(num_bytes=64):
    return os.urandom(num_bytes)

def unique_hash(num_bytes=64):
    b = os.urandom(num_bytes)
    h = binascii.hexlify(b)
    return h.decode('utf-8')
