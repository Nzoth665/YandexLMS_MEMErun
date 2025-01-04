import socket
from _thread import *
from main import *

heros = []
board = Board(600, 600, 5, screen, 50, 50)


# функция для обработки каждого клиента
def client_thread(con):
    while True:
        pass



server = socket.socket()
# hostname = socket.gethostname()
hostname = "localhost"
port = 12345
server.bind((hostname, port))
server.listen(4)

print("Server running")
while True:
    client, _ = server.accept()  # принимаем клиента
    heros.append(Hero())
    start_new_thread(client_thread, (client,))  # запускаем поток клиента