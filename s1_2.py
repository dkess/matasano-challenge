import base64
import util

a_a = "1c0111001f010100061a024b53535009181c"
b_a = "686974207468652062756c6c277320657965"

a_i = util.a2i(a_a)
b_i = util.a2i(b_a)

c_i = int(a_i ^ b_i)

c_a = util.i2a(c_i)

print(c_a)
print(util.b2s(util.a2b(c_a)))
