import socket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def main():
    # Initialize socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Generate RSA key pair for the client
    client_key = RSA.generate(2048)
    client_public_key = client_key.publickey()

    # Send client's public key to the server
    client_socket.sendall(client_public_key.export_key())

    # Instantiate PKCS1_OAEP cipher with server public key
    server_public_key = RSA.import_key(client_socket.recv(1024))
    cipher = PKCS1_OAEP.new(server_public_key)

    # Send encrypted message to the server
    message = "Hello, server!"
    encrypted_message = cipher.encrypt(message.encode())
    client_socket.sendall(encrypted_message)

    client_socket.close()

if __name__ == "__main__":
    main()
