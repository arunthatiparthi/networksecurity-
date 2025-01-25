import socket
import ssl

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
CERTFILE = 'server.crt'
KEYFILE = 'server.key'

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

# Load SSL context with server's certificate and private key
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

# Accept incoming connection and wrap it in SSL/TLS
print("Waiting for a connection...")
connection, client_address = server_socket.accept()
ssl_connection = context.wrap_socket(connection, server_side=True)

try:
    print(f"Connection from {client_address}")

    # Receive data from the client
    data = ssl_connection.recv(1024)
    print(f"Received: {data.decode()}")

    # Send data back to the client
    message = "Hello, client! This is a secure connection."
    ssl_connection.sendall(message.encode())
finally:
    # Close the SSL connection
    ssl_connection.close()
