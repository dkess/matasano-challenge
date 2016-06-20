import base64
import binascii

start = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

print("Starting with string "+start)

print("Converting hex to base64")

b = binascii.a2b_hex(start)
c = base64.b64encode(b)

print("Converted: "+c.decode("utf-8"))

print("The message was: "+b.decode("utf-8"))
