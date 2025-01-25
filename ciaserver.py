import socket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

def receive_message(conn):
    data = b""
    while True:
        packet = conn.recv(1024)
        if not packet:
            break
        data += packet
    return data

def main():
    # Initialize socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server listening on port", PORT)

    while True:
        conn, addr = server_socket.accept()
        print("Connected to", addr)

        # Receive public key from client
        client_public_key = RSA.import_key(receive_message(conn))

        # Instantiate PKCS1_OAEP cipher with client public key
        cipher = PKCS1_OAEP.new(client_public_key)

        # Receive encrypted message from client
        encrypted_message = receive_message(conn)

        # Decrypt message
        decrypted_message = cipher.decrypt(encrypted_message)

        print("Received message from client:", decrypted_message.decode())

        conn.close()

if __name__ == "__main__":
    main()