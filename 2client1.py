from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket
import base64
import hashlib
import hmac

# Key generation
encryption_key = hashlib.sha256(b'Arun').digest()

# HMAC generation function
def generate_hmac(message):
    if isinstance(message, str):
        message_bytes = bytes(message, 'utf-8')
    else:
        message_bytes = message
    hmac_message = hmac.new(encryption_key, message_bytes, hashlib.sha512).hexdigest()
    return hmac_message

# AES encryption function
def encrypt_message(raw):
    block_size = AES.block_size
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=encryption_key, mode=AES.MODE_CFB, iv=iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

# AES decryption function
def decrypt_message(enc):
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])))

# Server setup
host, port = "127.0.0.1", 1234
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    connection, address = server_socket.accept()
    while True:
        message = input("Enter the message:")
        hmac_message = generate_hmac(message)
        encrypted_message = encrypt_message(message)
        encrypted_hmac = encrypt_message(hmac_message)
        print(encrypted_message, encrypted_hmac)
        encrypted_total = encrypted_message + b"||" + encrypted_hmac
        connection.sendall(encrypted_total)
        data = connection.recv(1024)
        decrypted_data = decrypt_message(data).decode('utf-8')
        decrypted_message, hmac_decrypted = data.split(b"||")
        hmac_decrypted_1 = decrypt_message(hmac_decrypted)
        hmac_generated = generate_hmac(decrypted_data)
        if hmac_generated.encode('utf-8') == hmac_decrypted_1:
            print(f"The message is: {decrypted_data}")
        else:
            print("The message has been tampered")
