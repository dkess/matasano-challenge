import base64
import binascii

def repeating_key_xor(msg_b, key_b):
    """Encrypts a message (in bytes format) with a key (also in bytes format).
    Returns bytes."""
    l = len(key_b)
    return bytes(key_b[n % l] ^ c_i for n, c_i in enumerate(msg_b))

if __name__ == '__main__':
    msg1_b = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal".encode('utf-8')

    key_b = 'ICE'.encode('utf-8')

    print(binascii.hexlify(repeating_key_xor(msg1_b, key_b)))
