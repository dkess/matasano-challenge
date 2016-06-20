import base64

from Crypto.Cipher import AES

import util

key_b = b'YELLOW SUBMARINE'

cipher = AES.new(key_b, AES.MODE_ECB)

f = open('7.txt')
s = ''.join(l.strip() for l in f)
f.close()

enc_b = base64.standard_b64decode(s)

print(util.b2s(cipher.decrypt(enc_b)))
