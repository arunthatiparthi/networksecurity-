from ecdsa import SigningKey, VerifyingKey, NIST256p
import os

# Key generation
private_key = SigningKey.generate(curve=NIST256p)
public_key = private_key.verifying_key

# Key exchange (Elliptic Curve Diffie-Hellman)
alice_private_key = os.urandom(32)  # Generate a random private key for Alice
alice_public_key = NIST256p.generator * int.from_bytes(alice_private_key, 'big')  # Compute Alice's public key

bob_private_key = os.urandom(32)  # Generate a random private key for Bob
bob_public_key = NIST256p.generator * int.from_bytes(bob_private_key, 'big')  # Compute Bob's public key

shared_secret_alice = alice_private_key * int.from_bytes(bob_public_key.to_string(), 'big')
shared_secret_bob = bob_private_key * int.from_bytes(alice_public_key.to_string(), 'big')

# Digital signature (Elliptic Curve Digital Signature Algorithm)
message = b"Hello, World!"
signature = private_key.sign(message)
print("Signature:", signature.hex())

try:
    public_key.verify(signature, message)
    print("Signature is valid.")
except:
    print("Invalid signature.")
