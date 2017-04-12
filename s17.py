import base64
from itertools import chain, repeat

import util

options = list(map(base64.b64decode, [
    'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93',
]))

key_b = util.random_bytes(16)

def f1(n):
    iv = util.random_bytes(16)
    msg = options[n]
    enc = util.cbc_enc(util.pkcs7pad(msg, 16), key_b, iv=iv)
    return iv, enc

def f2(iv, ct):
    msg = util.cbc_dec(ct, key_b, iv=iv)
    try:
        util.strip_pkcs7(msg)
        return True
    except util.PKCS7Error:
        return False

for a in range(len(options)):
    iv, ct = f1(a)

    blocks = [iv] + util.make_chunks(ct, 16)

    # figure out the padding amount
    padding_amount = 1
    for n in range(0, 15):
        evil = util.xor_bytestring(chain(repeat(0, n), [1], repeat(0, 15 - n)),
                                   blocks[-2])
        evil_blocks = blocks[:-2] + [evil] + blocks[-1:]
        if not f2(evil_blocks[0], bytes(chain.from_iterable(evil_blocks[1:]))):
            padding_amount = 16 - n
            break

    final = []

    plain = [padding_amount] * padding_amount
    for n in range(len(blocks) - 1, 0, -1):
        for i in range(15 - padding_amount, -1, -1):
            plain.append(None)
            for g in range(256):
                plain[-1] = g
                evil_suffix = util.xor_bytestring(reversed(plain),
                                                  blocks[n - 1][i:])
                evil_suffix = util.xor_bytestring(evil_suffix,
                                                  [16 - i] * (16 - i))
                evil_block = blocks[n - 1][:i] + evil_suffix

                evil_blocks = chain(blocks[:n-1], [evil_block, blocks[n]])
                evil_blocks = blocks[:n-1] + [evil_block, blocks[n]]

                if f2(evil_blocks[0],
                      bytes(chain.from_iterable(evil_blocks[1:]))):
                    break

        final += plain

        plain = []
        padding_amount = 0

    print(util.strip_pkcs7(bytes(reversed(final))).decode())
