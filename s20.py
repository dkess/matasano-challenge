import base64

import util

# Mostly copied code from s6.py

ciphertexts = [base64.b64decode(l.strip()) for l in open('20.txt')]
min_len = min(len(ct) for ct in ciphertexts)
keysize = min_len

chunks = [ct[:min_len] for ct in ciphertexts]

key_chars = []
key_score = 0

for block in zip(*chunks):
    candidates = []
    for key_i in range(256):
        try:
            candidates.append((key_i, util.b2s(util.single_byte_xor(util.safe_bytes(block), key_i))))
        except UnicodeDecodeError:
            pass
    key, pt = max(candidates, key=lambda x: util.score_plaintext(x[1]))
    key_chars.append(key)
    key_score += util.score_plaintext(pt)

for chunk in chunks:
    msg_b = util.repeating_key_xor(chunk, key_chars)
    print(msg_b.decode())
