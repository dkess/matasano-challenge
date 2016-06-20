import binascii

from s1_3 import single_byte_xor, score_plaintext

candidates = []

with open('4.txt') as f:
    for l in f:
        l_a = l.strip()
        l_b = binascii.unhexlify(l_a)
        
        for key_i in range(256):
            try:
                candidates.append((l_a, key_i, single_byte_xor(l_b, key_i).decode('utf-8')))
            except UnicodeDecodeError:
                pass

print(max(candidates, key=lambda x: score_plaintext(x[2]))[2])
