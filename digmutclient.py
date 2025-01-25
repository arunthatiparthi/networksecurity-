import socket
from py_ecc.bls.ciphersuites import G2ProofOfPossession as bls_pop
def:
main():
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))
private_key = 5566
public_key = bls_pop.SkToPk(private_key)
client_socket.send(public_key) # Send the public key to the server
message = input('What to send: ').encode()
signature bls_pop.Sign(private_key, message)
client_socket.send(message)
client_socket.send(signature)
response client_socket.recv(1024) # Receive binary data directly
print(f"Server response: (response)")
client_socket.close()
main()
if __name=="__main__":
main()