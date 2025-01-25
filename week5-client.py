import socket
from py_ecc.bls import G2ProofOfPossession as bls_pop
from public_key import get_public_key
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    message = input("Enter the message:")
    client_socket.send(message.encode())
    signature = client_socket.recv(1024)
    public_key_server = get_public_key()
    is_valid = bls_pop.Verify(public_key_server, message.encode(), signature)
    if is_valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")
