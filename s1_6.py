import base64
import binascii
from itertools import combinations, zip_longest

from hamming import hamming
from s1_3 import single_byte_xor, score_plaintext
from s1_5 import repeating_key_xor

def safe_bytes(l):
    length = len(l)
    for i in range(length):
        if l[length - i - 1] != None:
            return bytes(l[:length - i])
    return bytes()

FILENAME = '6.txt'

s = ''
with open(FILENAME) as f:
    s = ''.join(l.strip() for l in f)

enc_b = base64.standard_b64decode(s)

candidates = []

for keysize in range(2, 40):
    a = enc_b[:keysize]
    b = enc_b[keysize:2*keysize]
    c = enc_b[keysize*3:keysize*4]
    d = enc_b[keysize*4:keysize*5]
    score = sum(hamming(x, y) for x, y in combinations([a, b, c, d], 2))
    candidates.append((keysize, score / keysize))

possible_sizes = [x[0] for x in sorted(candidates, key=lambda x: x[1])[:3]]

possible_keys = []
for keysize in possible_sizes:
    chunks = [list(enc_b)[i:i+keysize] for i in range(0, len(enc_b), keysize)]

    key_chars = []
    key_score = 0

    # zip_longest transposes the list of lists
    for block in zip_longest(*chunks):
        candidates = []
        for key_i in range(256):
            try:
                candidates.append((key_i, single_byte_xor(safe_bytes(block), key_i).decode('utf-8')))
            except UnicodeDecodeError:
                pass
        key, pt = max(candidates, key=lambda x: score_plaintext(x[1]))
        key_chars.append(key)
        key_score += score_plaintext(pt)
    possible_keys.append((bytes(key_chars), key_score))

key_b = max(possible_keys, key=lambda x: x[1])[0]
dec_b = repeating_key_xor(enc_b, key_b)
print('Key: {}\n------'.format(key_b.decode('utf-8')))
print(dec_b.decode('utf-8'))
