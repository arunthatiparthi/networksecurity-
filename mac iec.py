from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_and_hmac(message, key):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    
    # Create a Cipher object for AES encryption in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the message to match the block size of the encryption algorithm
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message) + padder.finalize()
    
    # Encrypt the padded message
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Compute the HMAC of the encrypted message
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(encrypted_data)
    hmac_digest = h.finalize()
    
    return iv + encrypted_data + hmac_digest

def verify_and_decrypt(ciphertext, key):
    # Split the ciphertext into IV, encrypted message, and HMAC
    iv = ciphertext[:16]
    encrypted_data = ciphertext[16:-32]
    received_hmac = ciphertext[-32:]
    
    # Create a Cipher object for AES decryption in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Verify the HMAC of the decrypted message
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(encrypted_data)
    h.verify(received_hmac)
    
    # Unpad the decrypted message
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data

# Example usage
message = b"Hello, world!"
key = os.urandom(32)  # Generate a random 256-bit key

# Encrypt and compute HMAC
ciphertext = encrypt_and_hmac(message, key)
print("Ciphertext:", ciphertext)

# Verify HMAC and decrypt
decrypted_message = verify_and_decrypt(ciphertext, key)
print("Decrypted message:", decrypted_message.decode())
