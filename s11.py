import random

import util

def encryption_oracle(msg_b):
    msg_b = (util.random_bytes(random.randrange(5,11))
             + msg_b
             + util.random_bytes(random.randrange(5, 11)))

    key_b = util.random_bytes(16)
    if random.getrandbits(1):
        # use ecb
        return (util.aes_ecb_enc(util.pkcs7pad(msg_b, 16), key_b), True)
    else:
        # use cbc
        return (util.cbc_enc(msg_b, key_b, iv=util.random_bytes(16)), False)

incorrect_guesses = 0
total = 200
for x in range(total):
    test = b'abc' * 200
    enc_b, is_ecb = encryption_oracle(test)
    if util.detect_ecb(enc_b) != is_ecb:
        incorrect_guesses += 1

if incorrect_guesses:
    print('Got {}/{} guesses wrong.{}'.format(incorrect_guesses, total))
else:
    print('We did it!')
