import socket
import pygame
from main import *


def client():
    client = socket.socket()
    hostname = "localhost"
    port = 12345
    client.connect((hostname, port))
    return client


if __name__ == '__main__':
    client = client()

    pygame.init()
    pygame.display.set_caption('MEMErun')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    clc = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

#client.send(message.encode())  # отправляем сообщение серверу
#data = client.recv(1024)  # получаем данные с сервера
# client.close()  # закрываем подключение
