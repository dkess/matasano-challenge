import util

if __name__ == '__main__':
    msg1_b = b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"

    key_b = b'ICE'

    print(util.b2a(util.repeating_key_xor(msg1_b, key_b)))
