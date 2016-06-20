import util


if __name__ == '__main__':
    a_a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    a_b = util.a2b(a_a)

    candidates = []
    for key_i in range(256):
        try:
            candidates.append((key_i, util.b2s(util.single_byte_xor(a_b, key_i))))
        except UnicodeDecodeError:
            pass

    print(max(candidates, key=lambda x: util.score_plaintext(x[1]))[1])
