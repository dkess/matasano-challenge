import util

candidates = []

f = open('4.txt')
for l in f:
    l_a = l.strip()
    l_b = util.a2b(l_a)
    
    for key_i in range(256):
        try:
            candidates.append((l_a, key_i, util.b2s(util.single_byte_xor(l_b, key_i))))
        except UnicodeDecodeError:
            pass
f.close()

print(max(candidates, key=lambda x: util.score_plaintext(x[2]))[2])
