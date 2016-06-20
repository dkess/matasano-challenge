import binascii
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
    i = 0
    for c in s:
        if c in ascii_letters or c in ' ,.\'"1234567890\n':
            i += 1
    return i

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

def pkcs7pad(b, size):
    """Pads a bytestring with \x04."""
    length = len(b)
    if size > length:
        return b + b'\x04' * (size - length)
    return b

ecb_cache = {}
def aes_ecb_enc(msg_b, key_b):
    try:
        return ecb_cache[key_b].encrypt(msg_b)
    except KeyError:
        cipher = AES.new(key_b, AES.MODE_ECB)
        ecb_cache[key_b] = cipher
        return cipher.encrypt(msg_b)

def aes_ecb_dec(enc_b, key_b):
    try:
        return ecb_cache[key_b].decrypt(enc_b)
    except KeyError:
        cipher = AES.new(key_b, AES.MODE_ECB)
        ecb_cache[key_b] = cipher
        return cipher.decrypt(enc_b)
