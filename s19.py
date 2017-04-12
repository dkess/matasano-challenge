import base64
from heapq import nlargest
from itertools import chain, product
from string import ascii_letters

# This code is really slow-- I'm not too proud of it.  Works with PyPy3 for
# faster execution.  Of course, Challenge 20 is supposed to be better than this
# anyways.

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

VALID_CHARS = set(r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890-=,.;:"!$()')
VALID_CHARS.add("'")
SIMPLE = set(ascii_letters + ' ')

ciphertexts = [base64.b64decode(l.strip()) for l in open('19.txt')]
max_len = max(len(ct) for ct in ciphertexts)

otp = []

# figure out each possible byte of the stream
for n in range(max_len):
    # guess all possibilities for the byte
    working_bytes = []
    for b in range(256):
        valid_byte = True
        for c in ciphertexts:
            if n < len(c) and chr(c[n] ^ b) not in VALID_CHARS:
                valid_byte = False
                break
        if valid_byte:
            working_bytes.append(b)
    otp.append(working_bytes)

def score_plaintexts(l):
    return sum(chr(c) in SIMPLE for c in chain.from_iterable(l))

for candidate in nlargest(10, ([xor(ct, stream) for ct in ciphertexts] for stream in product(*otp[:-8])), key=score_plaintexts):
    print(candidate)
