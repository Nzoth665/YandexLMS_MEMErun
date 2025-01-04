import pygame
import socket
import threading

# Set up Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Networked Multiplayer Client")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Client setup
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

# Send player position to server
def send_position(player):
    while True:
        position_data = f"{player.rect.centerx},{player.rect.centery}"
        client.send(position_data.encode())

# Game loop
player = Player(RED, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Start a thread for sending player data
thread = threading.Thread(target=send_position, args=(player,))
thread.start()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key inputs for movement
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Receive other player's position from server
    try:
        data = client.recv(1024).decode('utf-8')
        if data:
            x, y = map(int, data.split(","))
            # Handle the other player on screen (e.g., show it as a green square)
            pygame.draw.rect(screen, GREEN, (x, y, 50, 50))
    except:
        pass

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
client.close()
