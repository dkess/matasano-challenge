from urllib.parse import parse_qsl

import util

def cookie_parse(plaintext):
    return dict(parse_qsl(plaintext))

key_b = util.random_bytes(16)

def profile_for(email_b):
    if b'&' in email_b or b'=' in email_b:
        raise IndexError

    profile = b'email=' + email_b + b'&uid=10&role=user'

    return util.aes_ecb_enc(util.pkcs7pad(profile, 16), key_b)

def profile_decrypt(enc_b):
    return cookie_parse(util.aes_ecb_dec(enc_b, key_b))

# figure out the block size
start_len = len(profile_for(bytes()))
acc_bytes = b'a'
while True:
    new_len = len(profile_for(acc_bytes))
    if new_len != start_len:
        blocksize = new_len - start_len
        break
    else:
        acc_bytes += b'a'
print('Detected block size {}'.format(blocksize))

email_length = len(acc_bytes) + len(b'user')

our_email = b'a' * email_length
start_ciphertext = profile_for(our_email)[:-blocksize]

clear_len = len(acc_bytes) + 1
malicious_text = util.pkcs7pad(b'admin', blocksize)
out = profile_for((b'a' * clear_len) + malicious_text)
evil = util.make_chunks(out, blocksize)[1]

print(profile_decrypt(start_ciphertext + evil))
