import socket
import threading
from public_key import get_public_key
from py_ecc.bls import G2ProofOfPossession as bls_pop
private_key = 5678
HOST,PORT = "127.0.0.1",1234
def handle_client(conn,addr):
    data = conn.recv(1024).decode()
    print(f"Connected from client {addr}:{data}")
    signature = bls_pop.Sign(private_key,message=data.encode())
    conn.sendall(signature)
    conn.close()
def start_server():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST,PORT))
        server_socket.listen()
        print(f"Server listening from {PORT} port")        
        while True:
            conn,addr = server_socket.accept()
            threading.Thread(target=handle_client,args=(conn,addr)).start()
           
start_server()