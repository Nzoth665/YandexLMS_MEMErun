import socket
from threading import Thread

HOST, PORT = 'localhost', 1234  # Адрес сервера
MAX_PLAYERS = 4  # Максимальное кол-во подключений


class Server:
    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)

        self.max_players = max_conn
        self.players = []

        self.sock.listen(self.max_players)
        self.listen()

    def listen(self):
        while True:
            if not len(self.players) >= self.max_players:
                conn, addr = self.sock.accept()
                print("New connection", addr)
                Thread(target=self.handle_client,
                       args=(conn,)).start()

    def handle_client(self, conn):
        self.players.append(player)  # добавляем его в массив игроков

        while True:
            try:
                data = conn.recv(1024).decode()  # ждем запросов от клиента

                if not data:  # если запросы перестали поступать, то отключаем игрока от сервера
                    print("Disconnect")
                    break

            except Exception as e:
                print(e)
                break

        self.players.remove(self.player)  # если вышел или выкинуло с сервера - удалить персонажа


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)
