from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

key_pair = RSA.generate(2048)
private_key = key_pair.export_key()
public_key = key_pair.publickey().export_key()
message = b'Hello'
signature = pkcs1_15.new(RSA.import_key(private_key))
h = SHA256.new(message)
digital_signature = signature.sign(h)
encoded_signature = base64.b64encode(digital_signature).decode()
print("Digital Signature:", encoded_signature)
with open("private.pem", "wb") as f:
    f.write(private_key)

with open("public.pem", "wb") as f:
    f.write(public_key)