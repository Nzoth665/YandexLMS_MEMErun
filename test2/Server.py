import pygame
import socket
import threading

# Server setup
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen(2)  # Allow up to 2 clients

clients = []

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"[{addr}] {data}")
            # Send data back to both clients
            for c in clients:
                if c != client:
                    c.send(data.encode())
        except:
            break
    client.close()
    clients.remove(client)
    print(f"[{addr}] Disconnected.")

def start_server():
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")
    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

start_server()
