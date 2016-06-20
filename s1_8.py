import binascii

f = open('8.txt')
texts = [binascii.unhexlify(l.strip()) for l in f]
f.close()

# break the ciphertext into 16 byte chunks, and pick the one with the most
# repeated.  We do this by putting the chunks into a set, and seeing how big
# the set is.
sizes = [(t_b, len(set(tuple(t_b)[i:i+16] for i in range(0, len(t_b), 16))))
         for t_b in texts]

winner = min(sizes, key=lambda x: x[1])[0]

print(binascii.hexlify(winner).decode('utf-8'))
