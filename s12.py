import base64

import util

mystery_b = base64.b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""")

key_b = util.random_bytes(16)

def oracle(msg_b):
    return util.aes_ecb_enc(util.pkcs7pad(msg_b + mystery_b, 16), key_b)

# step 1: discover the block size
start_len = len(oracle(bytes()))
print(start_len)
acc_bytes = b'a'
while True:
    new_len = len(oracle(acc_bytes))
    if new_len != start_len:
        blocksize = new_len - start_len
        break
    else:
        acc_bytes += b'a'
print('Detected block size {}'.format(blocksize))

# step 2: detect that the function is using ECB
test_str = util.random_bytes(blocksize)
test_enc = oracle(test_str + test_str)
p1, p2 = util.make_chunks(test_enc, blocksize)[:2]
if p1 == p2:
    print('Oracle is using ECB')

enc_block_at = {}
dec_so_far = bytes()
for byte_num in range(start_len):
    if byte_num < blocksize:
        prepend = b'a' * (blocksize - byte_num - 1)
    else:
        prepend = dec_so_far[-blocksize + 1:]
    enc_chunks = util.make_chunks(oracle(prepend), blocksize)
    if byte_num < blocksize:
        for n, chunk in enumerate(enc_chunks[1:]):
            enc_block_at[byte_num + (n * blocksize)] = chunk
        want = enc_chunks[0]
    else:
        want = enc_block_at[byte_num - blocksize]
    if byte_num < blocksize:
        prepend += dec_so_far
    for b in range(256):
        if oracle(prepend + bytes([b]))[:blocksize] == want:
            dec_so_far += bytes([b])
            break

print()
print(util.b2s(dec_so_far))
