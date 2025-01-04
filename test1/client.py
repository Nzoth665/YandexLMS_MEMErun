import socket
from threading import Thread
import geme_classes

class Client:
    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr) # подключаемся к айпи адресу сервера

        self.board = geme_classes.Board(self.sock.recv(1024).decode())
        self.sprites = []
        Thread(target=self.get_players).start()

