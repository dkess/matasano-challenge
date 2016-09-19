import util

print(util.strip_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04"))

try:
    util.strip_pkcs7(b"ICE ICE BABY\x05\x05\x05\x05")
except util.PKCS7Error:
    print("test succeeded")
