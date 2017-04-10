import util

key_b = util.random_bytes(16)

PREFIX = b'comment1=cooking%20MCs;userdata=' 
SUFFIX = b';comment2=%20like%20a%20pound%20of%20bacon'
GOAL = b';admin=true;'

def f1(msg_b):
    b = PREFIX + msg_b + SUFFIX

    return util.cbc_enc(util.pkcs7pad(b, 16), key_b)

def has_admin(enc_b):
    msg_b = util.cbc_dec(enc_b, key_b)
    return GOAL in msg_b

normal = f1(b'')
switch = util.xor_bytestring(GOAL, (PREFIX + SUFFIX)[16:])
print(has_admin(switch + normal[len(switch):]))
