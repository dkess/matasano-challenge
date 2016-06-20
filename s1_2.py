import base64
import binascii

a_a = "1c0111001f010100061a024b53535009181c"
b_a = "686974207468652062756c6c277320657965"

a_i = int(a_a, 16)
b_i = int(b_a, 16)

c_i = int(a_i ^ b_i)

c_a = "{:x}".format(c_i)

print(c_a)
print(binascii.unhexlify(c_a).decode('utf-8'))
