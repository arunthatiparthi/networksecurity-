import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import hmac
import base64

server_host, server_port = "127.0.0.1", 1234
encryption_key = hashlib.sha256(b'Arun').digest()

def generate_hmac(message):
    if isinstance(message, str):
        message_bytes = bytes(message, 'utf-8')
    elif isinstance(message, bytes):
        message_bytes = message
    hmac_message = hmac.new(encryption_key, message_bytes, hashlib.sha512).hexdigest()
    return hmac_message

def encrypt_message(raw):
    block_size = AES.block_size
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=encryption_key, mode=AES.MODE_CFB, iv=iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt_message(enc):
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_host, server_port))
    while True:
        data = client_socket.recv(1024)
        decrypted_data = decrypt_message(data).decode('utf-8')
        decrypted_message, hmac_decrypted = data.split(b"||")
        hmac_decrypted_1 = decrypt_message(hmac_decrypted)
        hmac_generated = generate_hmac(decrypted_data)
        if hmac_generated == hmac_decrypted_1:
            print(f"The message is: {decrypted_data}")
        else:
            print("The message has been tampered")
        user_input = input("Enter the message:")
        hmac_msg = generate_hmac(user_input)
        encrypted_msg, encrypted_hmac = encrypt_message(user_input), encrypt_message(hmac_msg.decode('utf-8'))
        encrypted_total = encrypted_msg + b"||" + encrypted_hmac
        client_socket.sendall(encrypted_total)
