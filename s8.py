import util
import binascii

f = open('8.txt')
texts = []
for l in f:
         texts.append(util.a2b(l.strip()))
f.close()

# break the ciphertext into 16 byte chunks, and pick the one with the most
# repeated.  We do this by putting the chunks into a set, and seeing how big
# the set is.
sizes = [(t_b, len(set(tuple(chunk) for chunk in util.make_chunks(t_b, 16))))
         for t_b in texts]

winner = min(sizes, key=lambda x: x[1])[0]

print(util.b2a(winner).decode('utf-8'))
