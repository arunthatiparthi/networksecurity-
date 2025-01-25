from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import sys
import binascii

with open("public.pem", "rb") as f:
    public_key_pem = f.read()
public_key = RSA.import_key(public_key_pem)

encoded_signature = input("Enter Digital Signature: ")
try:
    digital_signature = base64.b64decode(encoded_signature.encode())
except (binascii.Error, UnicodeDecodeError):
    print("Invalid base64-encoded digital signature. Exiting...")
    sys.exit(1)

if len(digital_signature) % 4 != 0:
    print("Invalid base64-encoded digital signature. Exiting...")
    sys.exit(1)
    
message = b'Hello'

signature = pkcs1_15.new(public_key)
h = SHA256.new(message)
try:
    signature.verify(h, digital_signature)
    print("Digital Signature Verified")
except (ValueError, TypeError):
    print("Digital Signature Verification Failed")