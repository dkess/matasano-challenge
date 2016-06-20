import binascii

def hamming(a_b, b_b):
    return sum(bin(a_b[n] ^ b_b[n]).count('1') for n in range(len(a_b)))

if __name__ == '__main__':
    a = 'this is a test'
    b = 'wokka wokka!!!'

    print(hamming(a.encode('utf-8'), b.encode('utf-8')))
