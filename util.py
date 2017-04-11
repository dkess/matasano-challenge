import binascii
from itertools import repeat
import math
import random
from string import ascii_letters

from Crypto.Cipher import AES

def a2i(a):
    """Converts a string of hex char pairs to an int"""
    return int(a, 16)

def i2a(i):
    """Converts an int to a string of hex char pairs"""
    return '{:x}'.format(i)

def b2a(b):
    """Converts a bytestring to a string of hex char pairs"""
    return binascii.hexlify(b)

def a2b(a):
    """Converts a string of hex char pairs to a bytestring"""
    return binascii.unhexlify(a)

def b2s(b):
    """Converts a UTF-8 encoded bytestring to a regular string"""
    return b.decode('utf-8')

def s2b(s):
    """Converts a regular string to a UTF-8 encoded bytestring"""
    return s.encode('utf-8')

def single_byte_xor(enc_b, key_i):
    """Applies the single-byte key key_i to the encrypted text.
    Returns bytes."""
    return bytes(key_i ^ c_i for c_i in enc_b)

def score_plaintext(s):
    """ Takes a plaintext string and gives it an int score based on how
    comprehensible it is."""
    return sum(c in ascii_letters or c in ' ,.\'"1234567890\n' for c in s)

def repeating_key_xor(msg_b, key_b):
    """Encrypts a message (in bytes format) with a key (also in bytes format).
    Returns bytes."""
    l = len(key_b)
    return bytes(key_b[n % l] ^ c_i for n, c_i in enumerate(msg_b))

def hamming_dist(a_b, b_b):
    """Returns the hamming distance between two bytestrings."""
    return sum(bin(a_b[n] ^ b_b[n]).count('1') for n in range(len(a_b)))

def safe_bytes(l):
    """Converts an iterable to a bytestring, and removes trailing Nones"""
    length = len(l)
    for i in range(length):
        if l[length - i - 1] != None:
            return bytes(l[:length - i])
    return bytes()

def make_chunks(l, n):
    """Takes an iterable and breaks it up into chunks of length n.
    Example: make_chunks([1,2,3,4,5,6,7], 2) -> [[1,2], [3,4], [5,6], [7]]"""
    return [l[i:i+n] for i in range(0, len(l), n)]

def pkcs7pad(b, size=16):
    """Pads a bytestring."""
    padlen = ((size - len(b) - 1) % 16) + 1
    return b + bytes([padlen]) * padlen

ecb_cache = {}
def aes_ecb_enc(msg_b, key_b):
    try:
        cipher = ecb_cache[key_b]
    except KeyError:
        cipher = AES.new(key_b, AES.MODE_ECB)
        ecb_cache[key_b] = cipher
    return cipher.encrypt(msg_b)

def aes_ecb_dec(enc_b, key_b):
    try:
        cipher = ecb_cache[key_b]
    except KeyError:
        cipher = AES.new(key_b, AES.MODE_ECB)
        ecb_cache[key_b] = cipher
    return cipher.decrypt(enc_b)

def xor_bytestring(a_b, b_b):
    """XORs two bytestrings.  If one is longer than the other, it will be
    truncated to the length of the shortest bytestring."""
    return bytes(a ^ b for a, b in zip(a_b, b_b))

def cbc_enc(msg_b, key_b, iv=repeat(0), enc=aes_ecb_enc):
    o = bytes()
    last = iv
    for c in make_chunks(msg_b, 16):
        last = enc(xor_bytestring(pkcs7pad(msg_b, 16), last), key_b)
        o += last
    return o

def cbc_dec(enc_b, key_b, iv=repeat(0), dec=aes_ecb_dec):
    o = bytes()
    last = iv
    for c in make_chunks(enc_b, 16):
        o += xor_bytestring(dec(c, key_b), last)
        last = c
    return o

def random_bytes(length):
    return bytes(random.randrange(256) for _ in range(length))

def detect_ecb(enc_b):
    """Returns true if enc_b was probably encrypted with ECB"""
    uniq = len(set(tuple(chunk) for chunk in make_chunks(enc_b, 16)))
    length = math.ceil(len(enc_b) / 16)
    return uniq / length < 0.99

class PKCS7Error(Exception):
    pass

def strip_pkcs7(msg_b, size=16):
    padlen = msg_b[-1]

    if padlen > size or padlen == 0:
        raise PKCS7Error

    if msg_b[-padlen:] != bytes([padlen]) * padlen:
        raise PKCS7Error

    return msg_b[:-padlen]
