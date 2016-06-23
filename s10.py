import base64

import util

f = open('10.txt')
enc_b = base64.b64decode(''.join(f))
f.close()

key_b = b'YELLOW SUBMARINE'

msg_b = util.cbc_dec(enc_b, key_b)

print(util.b2s(msg_b))
