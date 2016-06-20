import base64
import binascii
from string import ascii_letters

def single_byte_xor(enc_b, key_i):
    """Applies the single-byte key key_i to the encrypted text.
    Returns bytes."""
    return bytes(key_i ^ c_i for c_i in enc_b)

def score_plaintext(s):
    """ Takes a plaintext string and gives it an int score based on how
    comprehensible it is."""
    i = 0
    for c in s:
        if c in ascii_letters or c in ' ,.\'"1234567890\n':
            i += 1
    return i

if __name__ == '__main__':
    a_a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    a_b = binascii.unhexlify(a_a)

    candidates = []
    for key_i in range(256):
        try:
            candidates.append((key_i, single_byte_xor(a_b, key_i).decode('utf-8')))
        except UnicodeDecodeError:
            pass

    print(max(candidates, key=lambda x: score_plaintext(x[1]))[1])
