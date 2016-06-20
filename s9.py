def pkcs7pad(b, size):
    length = len(b)
    if size > length:
        return b + b'\x04' * (size - length)
    return b

if __name__ == '__main__':
    start_b = b'YELLOW SUBMARINE'
    print(pkcs7pad(start_b, 20))
