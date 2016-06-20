import base64

from Crypto.Cipher import AES

key_s = 'YELLOW SUBMARINE'

cipher = AES.new(key_s.encode('utf-8'), AES.MODE_ECB)

s = ''
with open('7.txt') as f:
    s = ''.join(l.strip() for l in f)

enc_b = base64.standard_b64decode(s)

print(cipher.decrypt(enc_b).decode('utf-8'))
