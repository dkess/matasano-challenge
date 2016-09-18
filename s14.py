import base64
import random
import sys

import util

mystery_b = base64.b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""")

print(mystery_b[0])

blocksize = 16
key_b = util.random_bytes(16)

def oracle(msg_b):
    random_prefix = util.random_bytes(random.randrange(16))
    return util.aes_ecb_enc(util.pkcs7pad(
        random_prefix + msg_b + mystery_b, 16), key_b)

base = {}
while len(base) < 16:
    o = oracle(bytes(16))
    base[o[16:32]] = o[32:]

start_len = len(oracle(bytes()))
dec_so_far = bytes()
ordered_base = []
for byte_num in range(start_len):
    found = 0
    while not found:
        for b in range(1, 256):
            if byte_num < blocksize:
                prepend = bytes(blocksize - byte_num)
            else:
                prepend = bytes()
            check = oracle(prepend + dec_so_far[-16:] + bytes([b]))
            if byte_num < blocksize:
                remainder = base.pop(check[16:32], None)
                if remainder:
                    found = b
                    ordered_base.append(util.make_chunks(remainder, 16))
                    break
            else:
                if check[16:32] == ordered_base[byte_num % 16][(byte_num // 16) - 1]:
                    found = b
                    break
    dec_so_far += bytes([found])
    print(bytes([found]).decode('utf-8'), end="", flush=True)

#print(dec_so_far.decode('utf-8'))