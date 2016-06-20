import base64
from itertools import combinations, zip_longest

import util

f = open('6.txt')
s = ''.join(l.strip() for l in f)
f.close()

enc_b = base64.standard_b64decode(s)

candidates = []

for keysize in range(2, 40):
    a = enc_b[:keysize]
    b = enc_b[keysize:2*keysize]
    c = enc_b[keysize*3:keysize*4]
    d = enc_b[keysize*4:keysize*5]
    score = sum(util.hamming_dist(x, y) for x, y in combinations([a, b, c, d], 2))
    candidates.append((keysize, score / keysize))

possible_sizes = [x[0] for x in sorted(candidates, key=lambda x: x[1])[:3]]

possible_keys = []
for keysize in possible_sizes:
    chunks = util.make_chunks(enc_b, keysize)

    key_chars = []
    key_score = 0

    # zip_longest transposes the list of lists
    for block in zip_longest(*chunks):
        candidates = []
        for key_i in range(256):
            try:
                candidates.append((key_i, util.b2s(util.single_byte_xor(util.safe_bytes(block), key_i))))
            except UnicodeDecodeError:
                pass
        key, pt = max(candidates, key=lambda x: util.score_plaintext(x[1]))
        key_chars.append(key)
        key_score += util.score_plaintext(pt)
    possible_keys.append((bytes(key_chars), key_score))

key_b = max(possible_keys, key=lambda x: x[1])[0]
dec_b = util.repeating_key_xor(enc_b, key_b)
print('Key: {}\n------'.format(util.b2s(key_b)))
print(util.b2s(dec_b))
